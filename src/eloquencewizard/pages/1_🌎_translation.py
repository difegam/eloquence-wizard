"""
This module is the translation functionality of the app.
"""

import streamlit as st
from components.input_text import text_area_and_submit_button
from constants import Language, get_lang_index
from sidebar import sidebar
from translation import translate

languages = Language().default_lang()
language_names = tuple(languages.keys())

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

if (
    "dft_input_language" not in st.session_state
    and "dft_output_language" not in st.session_state
):
    st.session_state.dft_input_language = "English"
    st.session_state.dft_output_language = "Spanish"

    st.session_state.input_index = get_lang_index(
        language_names, st.session_state.dft_input_language
    )
    st.session_state.output_index = get_lang_index(
        language_names, st.session_state.dft_output_language
    )


def on_select_language():
    st.session_state.switch = False


switch = st.toggle("Switch", False, help="Switch language", key="switch")

if switch:
    st.session_state.input_index, st.session_state.output_index = (
        st.session_state.output_index,
        st.session_state.input_index,
    )

input_language = (
    st.selectbox(
        "Select language",
        language_names,
        placeholder="Select language...",
        index=st.session_state.input_index,
        key="input_language",
        on_change=on_select_language,
    )
    or "English"
)
st.session_state.dft_input_language = input_language
st.session_state.input_index = get_lang_index(language_names, input_language)

output_language = (
    st.selectbox(
        "Select language",
        language_names,
        placeholder="Select language...",
        key="output_language",
        index=st.session_state.output_index,
        on_change=on_select_language,
    )
    or "Spanish"
)
st.session_state.dft_output_language = output_language
st.session_state.output_index = get_lang_index(language_names, output_language)


text, summit_button = text_area_and_submit_button()

if summit_button:
    with st.spinner("Proofreading..."):
        output = translate(
            chat, text, input_language=input_language, output_language=output_language
        )
        st.write(output)
