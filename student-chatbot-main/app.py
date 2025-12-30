import streamlit as st
import os
from dotenv import load_dotenv
from models.mysql_manager import MySQLManager
from models.vector_manager import VectorManager
from models.llm_manager import LLMManager
from views.ui_components import render_sidebar, render_chat_message, render_header

load_dotenv()

def main():
    st.set_page_config(page_title="MySQL RAG Bot", page_icon="🤖", layout="wide")
    
    # Initialize managers
    mysql_mgr = MySQLManager()
    vector_mgr = VectorManager()
    llm_mgr = LLMManager()

    render_header()
    render_sidebar()

    # Session state for chat history and refresh
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "refresh_needed" not in st.session_state:
        st.session_state.refresh_needed = False

    # Handle data refresh from MySQL
    if st.session_state.refresh_needed:
        with st.spinner("Fetching data from MySQL and indexing..."):
            data = mysql_mgr.fetch_data()
            if data:
                vector_mgr.add_documents(data)
                st.success(f"Indexed {len(data)} records from MySQL.")
            else:
                st.warning("No data found in MySQL or connection failed.")
        st.session_state.refresh_needed = False

    # Display chat history
    for message in st.session_state.messages:
        render_chat_message(message["role"], message["content"])

    # User input
    if prompt := st.chat_input("Ask me anything about your database data:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_chat_message("user", prompt)

        with st.spinner("Generating answer..."):
            try:
                # 1. Retrieve context from Chroma
                context_docs = vector_mgr.query(prompt)
                
                # 2. Generate answer using Gemini
                if context_docs:
                    answer = llm_mgr.generate_answer(prompt, context_docs)
                else:
                    answer = "I couldn't find any relevant information in the database to answer your question."
                
                # 3. Display answer
                st.session_state.messages.append({"role": "assistant", "content": answer})
                render_chat_message("assistant", answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
