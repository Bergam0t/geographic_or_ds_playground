import streamlit as st
from app.utils import write_terminal_html, render_navigation, page_styling
from app.utils_investigations import DEPRIVATION
from app.maps import render_deprivation_map

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

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

st.title("Deprivation")

intro_text = """
    <br><br>

    You know that it has been found that women in more deprived areas have
        <br>- lower breast cancer incidence.
        <br>- significantly higher mortality rates.
        <br>- poorer screening uptake.

    <br><br>

    You ask your analyst to show deprivation and they deliver following map, but do not offer any interpretation.
    """

if not st.session_state.deprivation_page_visited:
    char_count, reveal_speed = write_terminal_html(
        intro_text,
        output_path="app/assets/terminal_working/deprivation_page.html",
    )
else:
    char_count, reveal_speed = write_terminal_html(
        intro_text,
        output_path="app/assets/terminal_working/deprivation_page.html",
        reveal_speed_ms=0,
    )

st.iframe("app/assets/terminal_working/deprivation_page.html")

render_deprivation_map()


st.subheader("Interpretation")
st.radio("Based on this map alone, where would you place the new centre?")

st.radio("What is your most important takeaway from this map?")


st.subheader("Write down any additional thoughts you have.")
st.caption("These will be saved to your notes.")
st.text_area(label="Your Thoughts", label_visibility="hidden")


render_navigation(DEPRIVATION)
