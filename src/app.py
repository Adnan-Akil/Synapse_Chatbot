"""Application for a Q&A chatbot using uploaded documents"""

try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
from config.config import Config
from utils import inject_custom_css
from components.sidebar import render_sidebar
from components.chat import initialize_chat, display_chat_history, handle_user_input

# 1. Page Config
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide"
)

# 2. Inject CSS
inject_custom_css()

# 3. Header
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-weight: 800; font-size: 3rem; background: linear-gradient(to right, #4cc9f0, #4361ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {Config.PAGE_TITLE} {Config.PAGE_ICON}
        </h1>
        <p style="font-size: 1.2rem; opacity: 0.8;">Premium RAG Assistant powered by {Config.LLM_MODEL_NAME}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. Sidebar
render_sidebar()

# 5. Chat Interface
initialize_chat()
display_chat_history()
handle_user_input()
