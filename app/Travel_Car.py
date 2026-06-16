import streamlit as st
from app.utils import (
    render_navigation,
    setup_lokigi_site_problem_car_existing,
    page_styling,
    load_devon_geography,
    load_population_weighted_centroids,
    TERMINAL_DEFAULT_SPEED,
    write_terminal_html,
)
from app.utils_investigations import TRAVEL_CAR
from app.maps import render_travel_maps
import time

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()


st.title("Travel Time - by Car")

problem = setup_lokigi_site_problem_car_existing()

solution = problem.solve(p=4)

best_solution_df = solution.return_best_combination_details()["problem_df"].iloc[0]


region_geometry = load_devon_geography()
pwc = load_population_weighted_centroids(snapped=True)

# st.write(best_solution_df)


best_solution_gdf = region_geometry.merge(
    best_solution_df, left_on="LSOA21NM", right_on="LSOA 2021 Name"
)


intro_text = f"""
> The analyst presents you with the following map of how long it takes to travel from the centre of each LSOA to its nearest site.
<br><br>
> They tell you that you can swap between each LSOA showing the travel time, the nearest centre, or colour each LSOA by whether it's within a certain travel time of its nearest centre using the buttons above the map.
<br><br>
> They scurry off quickly before you can ask any further questions, muttering something about needing to reticulate some splines.
<br><br>
> The map looms large on your screen. You must explore it yourself.
"""

char_count, reveal_speed = write_terminal_html(
    intro_text,
    output_path="app/assets/terminal_working/travel_car.html",
    reveal_speed_ms=TERMINAL_DEFAULT_SPEED,
)

st.iframe("app/assets/terminal_working/travel_car.html")

typing_duration = (char_count * reveal_speed) / 1000
time.sleep(typing_duration)

render_travel_maps(best_solution_gdf)

render_navigation(TRAVEL_CAR)
