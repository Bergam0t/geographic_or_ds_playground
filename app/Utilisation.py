import time
import streamlit as st
from app.utils import render_navigation, write_terminal_html, page_styling
from app.utils_investigations import UTILISATION

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("Current CDC Utilisation")

render_navigation(UTILISATION)
