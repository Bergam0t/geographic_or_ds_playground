import streamlit as st
from app.utils import (
    render_navigation,
    write_terminal_html,
    page_styling,
    select_site_from_current_evidence,
)
from app.utils_investigations import DEMAND
from app.maps import render_demand_map

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

if "site_submitted_demand" not in st.session_state:
    st.session_state.site_submitted_demand = False

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


@st.fragment
def selection_map():
    st_data = render_demand_map()

    st.write("From just the evidence on this page, which site would you choose?")

    selected_site = st_data["last_object_clicked_popup"]

    if "confirmed_site_demand" not in st.session_state:
        st.session_state.confirmed_site_demand = None

    if selected_site is None:
        st.warning(
            "Click on a blue candidate site on the map above to make your selection."
        )
        # Reset confirmation if no site is selected
        st.session_state.confirmed_site_demand = None
    elif st.session_state.site_submitted_demand:
        st.info(
            f"You have already submitted a site recommendation based on demand ({st.session_state.confirmed_site_demand['Site']})."
            "\n\nPlease use the buttons below to request your next analysis."
        )
    else:
        st.success(f"Selected Site = {selected_site}")
        st.session_state.confirmed_site_demand = {
            "What": "Demand",
            "Site": selected_site,
        }

    button = st.button(
        "Click here to confirm your site choice",
        disabled=True
        if (
            st.session_state.confirmed_site_demand is None
            or st.session_state.site_submitted_demand
        )
        else False,
    )

    if not button:
        st.write("")
        st.write("")

    if button:
        st.session_state.site_submitted_demand = True
        st.rerun()


selection_map()

if st.session_state.site_submitted_demand:
    render_navigation(DEMAND)
