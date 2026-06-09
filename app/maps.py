from app.utils import create_demand_gdf, create_deprivation_gdf, load_devon_sites
import streamlit as st
import folium
from streamlit_folium import st_folium


def add_sites_to_map(m, sites_gdf):
    existing_sites = sites_gdf[sites_gdf["Existing"] == "Yes"]
    proposed_sites = sites_gdf[sites_gdf["Existing"] == "No"]

    existing_group = folium.FeatureGroup(name="Existing CDCs")
    proposed_group = folium.FeatureGroup(name="Proposed CDCs")

    for _, row in existing_sites.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row["Facility_Name"],
            tooltip=row["Facility_Name"],
            icon=folium.Icon(
                icon="plus",
                prefix="fa",
                color="red",
            ),
        ).add_to(existing_group)

    for _, row in proposed_sites.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row["Facility_Name"],
            tooltip=row["Facility_Name"],
            icon=folium.Icon(
                icon="plus",
                prefix="fa",
                color="blue",
            ),
        ).add_to(proposed_group)

    existing_group.add_to(m)
    proposed_group.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m


def add_site_legend(m):
    legend_html = """
    <div class="site-maplegend" style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 180px;
        background-color: white;
        border: 2px solid grey;
        z-index: 9999;
        font-size: 14px;
        padding: 10px;
    ">
    <b>CDC Sites</b><br>

    <i class="fa fa-plus" style="color:red"></i>
    Existing CDC<br>

    <i class="fa fa-plus" style="color:blue"></i>
    Proposed CDC
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    m.get_root().header.add_child(
        folium.Element("""
        <style>
        .site-maplegend {
            color: black !important;
        }
        </style>
        """)
    )

    return m


@st.fragment
def render_deprivation_map():
    deprivation_gdf = create_deprivation_gdf()
    sites_gdf = load_devon_sites()

    # Create choropleth
    m = deprivation_gdf.explore(
        column="Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOA",
        tooltip=[
            "LSOA21NM",
            "Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOA",
        ],
        tooltip_kwds={
            "aliases": [
                "Area:",
                "IMD Decile (1 = most deprived):",
            ],
            "labels": True,
            "sticky": False,
        },
        legend_kwds={"caption": "IMD Decile (1 = most deprived)"},
        cmap="cividis_r",
        # scheme="UserDefined",
        categorical=True,
        name="IMD Deciles",
        # classification_kwds={"bins": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
    )

    # Workaround for legend colours
    m.get_root().header.add_child(
        folium.Element("""
        <style>
        .legend-labels {
            color: black !important;
        }

        .legend-title {
            color: black !important;
        }
        </style>
        """)
    )

    # Add point layer
    m = add_sites_to_map(m, sites_gdf=sites_gdf)
    m = add_site_legend(m)

    st_folium(m, use_container_width=True)


@st.fragment
def render_demand_map():
    demand_gdf = create_demand_gdf()
    sites_gdf = load_devon_sites()

    selected_age_range = st.radio(
        "Select Age Range to Visualise",
        [
            "MF50-84",
            "F50-84",
            "M50-84",
        ],
        index=0,
    )
    # Create choropleth
    m = demand_gdf.explore(
        column=selected_age_range,
        tooltip=[
            "LSOA21NM",
            selected_age_range,
            "Total",
        ],
        tooltip_kwds={
            "aliases": [
                "Area:",
                "Expected Demand:",
                "Total Population:",
            ],
            "labels": True,
            "sticky": False,
        },
    )

    # Add point layer
    m = add_sites_to_map(m, sites_gdf=sites_gdf)
    m = add_site_legend(m)

    st_folium(m, use_container_width=True)
