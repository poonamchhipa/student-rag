import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Settings")
        st.info("Ensure your `.env` file is configured with the correct MySQL and Gemini API details.")
        if st.button("Refresh Data from MySQL"):
            st.session_state.refresh_needed = True

def render_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

def render_header():
    st.title("🤖 MySQL RAG Bot")
    st.markdown("---")
