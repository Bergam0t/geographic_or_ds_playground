import streamlit as st
from app.utils import render_navigation, write_terminal_html
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

intro_text = f"""
> Your analyst has delivered the following map.
<br><br>
> They tell you that you can hover over the red icons (the current CDCs) and the blue icons (the CDCs) to find out more.
<br><br>
> They also tell you that you can hover over each 
<br><br>
> They let you know that yellow is the highest demand, and purple means lower demand.
<br><br>
> You can use the + and - buttons in the top left to zoom in and out. 
"""

char_count, reveal_speed = write_terminal_html(
    intro_text,
    output_path="app/assets/terminal_working/demand.html",
)

st.iframe("app/assets/terminal_working/demand.html", height=300)

render_demand_map()

render_navigation(DEMAND)
