import streamlit as st
from retrieval import retrieve_similar_docs
from llm import final_answer

def initialize_chat():
    """Initialize session state for chat"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm your AI assistant. Upload documents to begin chatting.",
                "avatar": "🤖",
            }
        ]

def display_chat_history():
    """Display previous messages"""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar", "🤖")):
            st.write(msg["content"])

def handle_user_input():
    """Handle new user input and generate response"""
    if prompt := st.chat_input("Ask about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🧠 Thinking & Retrieving..."):
                try:
                    similar_chunks = retrieve_similar_docs(prompt)
                    if similar_chunks:
                        answer = final_answer(similar_chunks, prompt)
                        st.write(answer)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": answer, "avatar": "🤖"}
                        )
                    else:
                        warning_msg = "I couldn't find relevant information in the uploaded documents."
                        st.warning(warning_msg)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": warning_msg, "avatar": "🤖"}
                        )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
