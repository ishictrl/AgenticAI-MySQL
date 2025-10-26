import streamlit as st
from code import create_db_agent, query_database

st.title("AtliQ T Shirts: Database Q&A 👕")

def get_agent():
    return create_db_agent()

try:
    agent = get_agent()
    question = st.text_area(
        "Your question:",
        height=100,
        placeholder="Example: How many white Nike t-shirts in size M do we have?"
    )
    if st.button("🔍 Get Answer", type="primary"):
        if question:
            with st.spinner("Thinking..."):
                answer = query_database(agent, question)
                st.success("Answer:")
                st.write(answer)
        else:
            st.warning("Please enter a question!")
except Exception as e:
    st.error(f"Error: {e}")



