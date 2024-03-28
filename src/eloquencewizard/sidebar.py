import re

import streamlit as st
from faq import faq


def sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            ## How to use
            1. Connect to the VPN🔒
            2. Enter Bridge ID and press enter👇🏽
            3. Enjoy the tool🎉
            """
        )
        st.text_input(
            "Bridge ID:",
            key="bridge_id",
            placeholder="bridge",
            value=st.session_state.get("bridge_id", ""),
            max_chars=4,
        )
        bridge_id = st.session_state.get("bridge_id")

        if bridge_id and not re.match(r"^.*[0-9A-F]{4}$", bridge_id):
            st.error("Invalid bridge ID")

        st.markdown(
            """
            ## 🛠 Tools
            - 📈 [**Status Over Time**](https://gw-mgmt.sensorfact.nl/monitoring/d/a2tqxITWz/status-over-time-map)
            - 📱 [**Whereversim**](https://portal.whereversim.de/connected-devices)
            """
        )

        st.markdown("---")
        st.markdown("# About")
        st.markdown("---")
        faq()
