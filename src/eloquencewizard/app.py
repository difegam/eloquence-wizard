"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from annotated_text import annotated_text
from src.eloquencewizard.proofread import proofread, text_differences
from settings import settings
from sidebar import sidebar

st.set_page_config(page_title="Eloquence Wizard", page_icon="🧙‍♂️", layout="centered")
st.header(":orange[Eloquence] :rainbow[Wizard] 🧙‍♂️", divider="rainbow")

sidebar()


def annotated_text_(text: str, differences: set[str]):
    annotated_text(
        text,
        [(word, "error") if word in differences else word for word in text.split()],
    )


text_area = st.text_area(
    "Enter text:",
    height=200,
    placeholder="Type something...",
    key="text_area",
    help="Enter text to proofread",
    value="How kan I fidn to the nearest hospital?",
)

summit_button = st.button("Submit", key="submit")

if summit_button:
    with st.spinner("Proofreading..."):
        output = proofread(settings.llm, text_area)
        differences = text_differences(output.corrected_text, text_area)
        l = [(error.incorrect, error.error_type) for error in output.errors]

        st.write(f"{output.corrected_text}")
        annotated_text(*l)


st.divider()
with st.expander("Advanced Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")
