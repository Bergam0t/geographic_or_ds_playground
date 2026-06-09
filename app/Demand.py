import streamlit as st
from app.utils import render_navigation
from app.utils_investigations import DEMAND
from app.maps import render_demand_map

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

st.title("Demand")

render_demand_map()

render_navigation(DEMAND)
