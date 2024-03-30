import streamlit as st
from components.input_text import text_area_and_submit_button
from sidebar import sidebar
from translation import translate

sidebar()

st.markdown(
    """
# Translate 🌎
"""
)
chat = st.session_state.chat

if chat is None:
    st.error("Please select a provider and model in the sidebar.")
    st.stop()

text, summit_button = text_area_and_submit_button()

if summit_button:
    with st.spinner("Proofreading..."):
        output = translate(chat, text, input_language="en", output_language="es")
        st.write(output)
