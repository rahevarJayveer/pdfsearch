css = """
<style>
    .stApp { padding-top: 1rem; }

    .message {
        padding: 10px 16px;
        border-radius: 18px;
        line-height: 1.4;
        max-width: 80%;
        word-wrap: break-word;
        margin-bottom: 8px;
    }

    .user-message {
        background-color: #4f46e5;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .bot-message {
        background-color: #f3f4f6;
        color: #1f2937;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #5A4BFF;
    }

    .sidebar .stImage {
        border-radius: 8px;
        border: 1px solid #5A4BFF;
    }

    .stTextInput>div>div>input {
        border-radius: 24px !important;
        padding: 12px 16px !important;
    }
</style>
"""

bot_template = """
<div class="message bot-message">
    {{MSG}}
    <div class="timestamp">AI Assistant</div>
</div>
"""

user_template = """
<div class="message user-message">
    {{MSG}}
    <div class="timestamp">You</div>
</div>
"""
