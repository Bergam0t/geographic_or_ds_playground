import streamlit as st
from app.utils import render_navigation, page_styling
from app.utils_investigations import ISOCHRONES_CAR


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("Isochrones")

render_navigation(ISOCHRONES_CAR)
