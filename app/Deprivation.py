import streamlit as st
import geopandas
from streamlit_folium import st_folium
from app.utils import load_devon_geography, load_deprivation, write_terminal_html

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

st.title("Deprivation")

intro_text = """
    It has been found that women in more deprived areas have lower breast cancer incidence but significantly higher mortality rates.
    <br><br>
    You find that screening uptake is poorer among those in more deprived areas.
    <br><br>
    You want to ensure that you are considering deprivation in your findings, so you ask your HSMA to bring the deprivation data in too.
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


@st.cache_data
def create_deprivation_gdf():
    devon_gdf = load_devon_geography()
    deprivation_df = load_deprivation()
    full_gdf = devon_gdf.merge(
        deprivation_df, left_on="LSOA21NM", right_on="LSOA name (2021)"
    )
    return full_gdf


deprivation_gdf = create_deprivation_gdf()


@st.fragment
def render_deprivation_map():
    st_folium(
        deprivation_gdf.explore(
            column="Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOA"
        ),
        use_container_width=True,
    )


render_deprivation_map()
