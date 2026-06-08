import time
import streamlit as st
from app.utils import write_terminal_html, record_page_visited

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
> You have been assigned a junior analyst who can provide information, but you must decide what evidence to review and can only send one request at a time.
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

record_page_visited("app/Homepage.py")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "'Can you give me a map of travel times to existing CDCs?'",
        use_container_width=True,
    ):
        st.session_state.nav_history.append("Travel Times Map")
        st.switch_page("app/Travel_Car.py")

with col2:
    if st.button(
        "'Can you show me a map of deprivation across Devon?'", use_container_width=True
    ):
        st.session_state.nav_history.append("Deprivation Map")
        st.switch_page("app/Deprivation.py")

with col3:
    if st.button(
        "'Can you give me a map of demand across Devon in the 50-85 age range?'",
        use_container_width=True,
    ):
        st.session_state.nav_history.append("Demand Map")
        st.switch_page("app/Demand.py")

st.caption("More briefing options will be unlocked as you uncover additional evidence.")
