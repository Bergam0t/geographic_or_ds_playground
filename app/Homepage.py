import time
import streamlit as st
from app.utils import write_terminal_html, investigation_button
from app.utils_investigations import DEMAND, TRAVEL_CAR, DEPRIVATION

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

st.title("Welcome")

intro_text = """
> You are a senior manager who has been given funding for an additional community diagnostic centre (CDC) in Devon.
<br><br>
> You have been told to improve access for those between 50 and 85.
<br><br>
> People may only use CDCs within Devon. They cannot cross the Devon border to access a different CDC.
<br><br>
> You have been assigned a junior analyst who can provide information, but can only follow specific instructions.
<br><br>
> Due to capacity constraints, your analyst can provide you with a maximum of four briefings on areas of your choosing.
<br><br>
> What would you like your first briefing to be on?
"""

if not st.session_state.homepage_visited:
    char_count, reveal_speed = write_terminal_html(
        intro_text,
        output_path="app/assets/terminal_working/homepage.html",
    )
else:
    char_count, reveal_speed = write_terminal_html(
        intro_text,
        output_path="app/assets/terminal_working/homepage.html",
        reveal_speed_ms=0,
    )

st.iframe("app/assets/terminal_working/homepage.html")

typing_duration = (char_count * reveal_speed) / 1000
time.sleep(typing_duration)

col1, col2, col3 = st.columns(3)

with col1:
    investigation_button(DEMAND)

with col2:
    investigation_button(DEPRIVATION)

with col3:
    investigation_button(TRAVEL_CAR)
