import streamlit as st
from app.utils import render_navigation, page_styling
from app.utils_investigations import TWO_SFCA_CAR


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("2 Step Floating Catchment Areas")

render_navigation(TWO_SFCA_CAR)
