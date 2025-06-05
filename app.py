import tempfile
import streamlit as st
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from htmlTemplates import css, bot_template, user_template

# ----- Helper Functions -----

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            if page_text := page.extract_text():
                text += page_text
    return text

def get_text_chunks(text):
    return CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200
    ).split_text(text)

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

def show_pdf_preview(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(pdf_file.getvalue())
        try:
            image = convert_from_bytes(open(tmp.name, 'rb').read(), first_page=1, last_page=1)[0]
            st.image(image, caption=f"Preview: {pdf_file.name}", use_column_width=True)
        except Exception as e:
            st.error(f"Couldn't generate preview: {str(e)}")

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    for i, message in enumerate(response['chat_history']):
        template = user_template if i % 2 == 0 else bot_template
        st.write(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

# ----- Main App -----

def main():
    st.set_page_config(page_title="PDF Chat Assistant", layout="wide")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header(" PDF Chat Assistant")
    st.caption("Upload PDFs and chat with their content")

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

        if pdf_docs:
            st.success(f"{len(pdf_docs)} file(s) uploaded")
            for pdf in pdf_docs:
                with st.expander(f"{pdf.name}", expanded=False):
                    with st.spinner("Generating preview..."):
                        show_pdf_preview(pdf)

        if st.button("Process Documents"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        if not raw_text.strip():
                            st.error("No text could be extracted. Try different files.")
                            return
                        chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(chunks)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.success("Processing complete! Ask me anything about your documents.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please upload PDF files first")

    user_question = st.chat_input("Ask a question about your PDFs...")
    if user_question and st.session_state.conversation:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()
