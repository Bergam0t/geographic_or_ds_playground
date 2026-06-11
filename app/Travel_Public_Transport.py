import streamlit as st
from app.utils import (
    render_navigation,
    load_devon_geography,
    setup_lokigi_site_problem_pt,
)
from app.utils_investigations import TRAVEL_PT
from app.maps import render_travel_existing_map


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

st.title("Travel")

problem = setup_lokigi_site_problem_pt()

solution = problem.solve(p=4)

best_solution_df = solution.return_best_combination_details()["problem_df"].iloc[0]

region_geometry = load_devon_geography()

st.write(best_solution_df)

best_solution_gdf = region_geometry.merge(
    best_solution_df, left_on="LSOA21NM", right_on="LSOA 2021 Name"
)

render_travel_existing_map(best_solution_gdf)


render_navigation(TRAVEL_PT)


# """Your analyst has now used the phrase "transport modelling is more complicated
# than people realise" on seventeen separate occasions."
