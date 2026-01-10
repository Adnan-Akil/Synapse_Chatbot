import streamlit as st
from data_loader import document_handler
from file_parser import build_index, clear_vector_store, vector_store

def render_sidebar():
    """Renders the sidebar for document upload and management"""
    with st.sidebar:
        st.markdown("### 🗂️ Document Manager")
        
        # File Uploader
        uploaded_docs = st.file_uploader(
            label="Upload PDF, DOCX, TXT", 
            accept_multiple_files=True,
            help="Supported formats: .pdf, .docx, .txt, .csv, .xlsx"
        )
        
        # Process Button
        if st.button("🚀 Process Documents", use_container_width=True):
            if not uploaded_docs:
                st.warning("⚠️ Please upload files first.")
            else:
                with st.spinner("🔮 Processing & Indexing..."):
                    clear_vector_store(vector_store)
                    for file in uploaded_docs:
                        processed = document_handler(file)
                        build_index(processed)
                    st.success("✅ Knowledge Base Updated!")

        st.markdown("---")
        
        # Clear Chat Button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            if len(st.session_state.get("messages", [])) <= 1:
                st.toast("Chat is already empty!", icon="ℹ️")
            else:
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": "Hi! I'm your AI assistant. Ready to explore your documents?",
                        "avatar": "🤖",
                    }
                ]
                st.rerun()
