import streamlit as st
import geopandas
from streamlit_folium import st_folium
from app.utils import load_devon_geography, load_demand

st.title("Demand")
st.set_page_config(layout="wide")


@st.cache_data
def create_demand_gdf():
    devon_gdf = load_devon_geography()
    demand_df = load_demand()
    full_gdf = devon_gdf.merge(demand_df, left_on="LSOA21NM", right_on="LSOA 2021 Name")
    return full_gdf


demand_gdf = create_demand_gdf()

# st.write(demand_gdf)


@st.fragment
def render_demand_map():
    selected_age_range = st.radio(
        "Select Age Range to Visualise",
        [
            # "F18-49",
            # "M18-49",
            "F50-70",
            # "M50-70",
            # "F71+",
            # "M71+",
            # "Total",
            "F50-70 Percentage of Total LSOA Population",
        ],
        index=0,
    )
    st_folium(demand_gdf.explore(column=selected_age_range), use_container_width=True)


render_demand_map()
