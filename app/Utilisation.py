import time
import streamlit as st
from app.utils import render_navigation, write_terminal_html
from app.utils_investigations import UTILISATION

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Current CDC Utilisation")

render_navigation(UTILISATION)
