"""
Created on Tue Mar  8 10:50:12 2022
This file contains the text area component and a summit button.
"""

from typing import Callable

import streamlit as st


def text_area_and_submit_button(
    help="",
    on_click: Callable = lambda: None,
) -> tuple[str, bool]:

    text_area = st.text_area(
        "How can I help you today?",
        height=150,
        placeholder="Type something...",
        key="text_area",
        help=help,
    )

    summit_button = st.button("Submit 🪄", key="submit", on_click=on_click)

    return text_area, summit_button
