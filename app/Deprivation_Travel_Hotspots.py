import streamlit as st
from app.utils import render_navigation, page_styling
from app.utils_investigations import HOTSPOTS_DEPRIVATION_TRAVEL


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("Demand and Deprivation Hotspots")

render_navigation(HOTSPOTS_DEPRIVATION_TRAVEL)
