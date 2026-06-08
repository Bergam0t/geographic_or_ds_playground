import html
import streamlit as st
from app.utils import write_terminal_html

st.title("Welcome")

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

intro_text = """
> This is a simplified example showing how geographic optimisation can support service planning.
<br><br>
> You have been given funding for an additional community diagnostic centre in Devon.
<br><br>
> You have been told to focus on access for those between 50 and 85.
<br><br>
> How do you wish to proceed?
"""

write_terminal_html(
    intro_text,
    output_path="app/assets/terminal_working/homepage.html",
    reveal_speed_ms=30,
)

st.iframe("app/assets/terminal_working/homepage.html")
