import time
import streamlit as st
from app.utils import write_terminal_html, record_page_visited
from app.utils import render_navigation
from app.utils_investigations import PROJECTED_DEMAND


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

st.title("Projected Demand")

render_navigation(PROJECTED_DEMAND)
