import streamlit as st
import geopandas
from streamlit_folium import st_folium
from app.utils import create_demand_gdf, render_navigation
from app.utils_investigations import DEMAND

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


demand_gdf = create_demand_gdf()


@st.fragment
def render_demand_map():
    selected_age_range = st.radio(
        "Select Age Range to Visualise",
        [
            "MF50-84",
            "F50-84",
            "M50-84",
        ],
        index=0,
    )
    st_folium(demand_gdf.explore(column=selected_age_range), use_container_width=True)


render_demand_map()

render_navigation(DEMAND)
