"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from annotated_text import annotated_text
from proofread import proofread
from settings import settings
from sidebar import sidebar

st.set_page_config(page_title="Eloquence Wizard", page_icon="🧙‍♂️", layout="centered")
st.header(":orange[Eloquence] :rainbow[Wizard] 🧙‍♂️", divider="rainbow")

sidebar()

st.markdown(
    """
This is Eloquence Wizard.
"""
)


st.divider()
with st.expander("Advanced Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")
