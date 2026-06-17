from app.utils import (
    create_demand_gdf,
    create_deprivation_gdf,
    load_devon_sites,
    load_population_weighted_centroids,
)
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd


###########################
# MARK: Helpers
###########################
def add_sites_to_map(m, sites_gdf, add_centroids=False, centroid_gdf=None):
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

    if add_centroids:
        centroids = folium.FeatureGroup(name="Centroids")
        centroid_gdf = centroid_gdf.to_crs("EPSG:4326")

        for _, row in centroid_gdf.iterrows():
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x], color="white", radius=3
            ).add_to(centroids)

        centroids.add_to(m)

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


###########################
# MARK: Deprivation
###########################
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


###########################
# MARK: Demand
###########################
def render_demand_map():
    demand_gdf = create_demand_gdf()
    sites_gdf = load_devon_sites()

    raw_options = ["MF50-84", "Total"]

    alias_dict = {
        "MF50-84": "Per-LSOA Population - Between 50 and 84",
        "Total": "Total Per-LSOA Population",
    }

    selected_age_range = st.radio(
        "Select Age Range to Visualise",
        raw_options,
        format_func=lambda x: alias_dict.get(x, x),
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
        name="Population",
        zoom_start=9,
        scheme="Percentiles",
    )

    # Add point layer
    m = add_sites_to_map(m, sites_gdf=sites_gdf)
    m = add_site_legend(m)
    for child in m._children.values():
        if child == "color_scale" or hasattr(child, "caption"):
            # Default is usually ~450px. Let's make it thinner/wider:
            child.width = 800

    return st_folium(m, use_container_width=True)


###########################
# MARK: Travel
###########################
def render_travel_existing_map(best_solution_gdf, what, threshold=None):

    sites_gdf = load_devon_sites()

    centroids = load_population_weighted_centroids()

    if what == "time":
        column = "min_cost"
        name = "Travel Time (Minutes)"
        legend_kwds = {"caption": "Travel Time (Minutes)"}
        cmap = None
    elif what == "centre":
        column = "selected_site"
        name = "Nearest Site"
        legend_kwds = {"caption": "Nearest Site to LSOA"}
        cmap = None
    if what == "threshold":
        if threshold is None:
            raise ValueError("No threshold defined")
        else:
            best_solution_gdf["exceeds_threshold"] = (
                best_solution_gdf["min_cost"] > threshold
            ).map({True: "Yes", False: "No"})

            best_solution_gdf["exceeds_threshold"] = pd.Categorical(
                best_solution_gdf["exceeds_threshold"],
                categories=["No", "Yes"],
                ordered=True,
            )
            column = "exceeds_threshold"
            name = "Exceeds threshold time"
            legend_kwds = {"caption": f"Exceeds travel time of {threshold} minutes"}
            cmap = {
                "Yes": "#ef8a62",  # soft red/orange
                "No": "#67a9cf",  # soft blue
            }

            from matplotlib.colors import ListedColormap

            cmap = ListedColormap(["#67a9cf", "#ef8a62"])

    m = best_solution_gdf.round(1).explore(
        column=column,
        tooltip=["LSOA21NM", "min_cost", "selected_site"],
        tooltip_kwds={
            "aliases": [
                "Area:",
                "Travel time to nearest site (minutes):",
                "Nearest site:",
            ],
            "labels": True,
            "sticky": False,
        },
        name=name,
        zoom_start=9,
        legend_kwds=legend_kwds,
        cmap=cmap,
    )

    if what == "centre" or what == "threshold":
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
    m = add_sites_to_map(
        m,
        sites_gdf=sites_gdf,
        # Can turn centroids back on for debugging purposes if needed
        centroid_gdf=centroids,
        add_centroids=False,
    )
    m = add_site_legend(m)
    for child in m._children.values():
        if child == "color_scale" or hasattr(child, "caption"):
            # Default is usually ~450px. Let's make it thinner/wider:
            child.width = 800

    return st_folium(m, use_container_width=True)


def render_travel_maps(best_solution_gdf):
    map_selection = st.radio(
        "Select map type",
        [
            "Show travel time",
            "Show nearest centre",
            "Show regions exceeding a certain travel time",
        ],
    )

    if map_selection == "Show travel time":
        return render_travel_existing_map(best_solution_gdf, what="time")
    elif map_selection == "Show nearest centre":
        return render_travel_existing_map(best_solution_gdf, what="centre")
    elif map_selection == "Show regions exceeding a certain travel time":
        threshold = st.slider(
            label="Choose a maximum travel time",
            min_value=15,
            max_value=60,
            value=45,
            step=5,
        )
        return render_travel_existing_map(
            best_solution_gdf, what="threshold", threshold=threshold
        )
