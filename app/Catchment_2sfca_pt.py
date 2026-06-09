import streamlit as st
from app.utils import render_navigation
from app.utils_investigations import TWO_SFCA_PT


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

st.title("2 Step Floating Catchment Areas")

render_navigation(TWO_SFCA_PT)
