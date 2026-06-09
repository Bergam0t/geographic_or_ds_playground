import streamlit as st
from app.utils import render_navigation
from app.utils_investigations import HOTSPOTS_DEMAND


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

st.title("Demand and Deprivation Hotspots")

render_navigation(HOTSPOTS_DEMAND)
