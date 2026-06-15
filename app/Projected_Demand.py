import time
import streamlit as st
from app.utils import (
    write_terminal_html,
    record_page_visited,
    render_navigation,
    page_styling,
)
from app.utils_investigations import PROJECTED_DEMAND


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("Projected Demand")

render_navigation(PROJECTED_DEMAND)
