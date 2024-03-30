import streamlit as st
from components.input_text import text_area_and_submit_button
from proofread import proofread
from sidebar import sidebar

sidebar()

st.markdown(
    """
# Proofread Text 📝
"""
)
chat = st.session_state.chat

if chat is None:
    st.error("Please select a provider and model in the sidebar.")
    st.stop()

text, summit_button = text_area_and_submit_button()

if summit_button:
    with st.spinner("Proofreading..."):
        output = proofread(chat, text)
        st.write(f"{output.corrected_text}")
