import streamlit as st
from app.utils import (
    render_navigation,
    write_terminal_html,
    page_styling,
    select_site_from_current_evidence,
)
from app.utils_investigations import DEMAND
from app.maps import render_demand_map, make_selection_map

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("Demand")

intro_text = """
> Your analyst has delivered the following map.
<br><br>
> They tell you that you can hover over the red icons (the current CDCs) and the blue icons (the CDCs) to find out more.
<br><br>
> They also tell you that you can hover over each region to see the exact count of people 50-84 in the region.
<br><br>
> They let you know that yellow is the highest demand, and purple means lower demand.
<br><br>
> You can use the + and - buttons in the top left to zoom in and out.
"""

char_count, reveal_speed = write_terminal_html(
    intro_text,
    output_path="app/assets/terminal_working/demand.html",
)

st.iframe("app/assets/terminal_working/demand.html", height=275)

demand_selection_map = make_selection_map(render_demand_map, "demand")
demand_selection_map()

if st.session_state.site_submitted_demand:
    render_navigation(DEMAND)
