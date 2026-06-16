import streamlit as st
from app.utils import page_styling, load_devon_sites
import time
from PIL import Image
import pandas as pd
import pickle

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
page_styling()

st.title("Optimise")

# TODO: HARDCODED for development purposes
selected_site = "Okehampton - Exeter Road Industrial Estate"


def get_gif_duration(filename):
    with Image.open(filename) as gif:
        total_duration_ms = 0

        try:
            while True:
                total_duration_ms += gif.info.get("duration", 100)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

    return total_duration_ms / 1000


gif_path = "data/solution_car_5.gif"

with open("data/solution_car_5.pkl", "rb") as f:
    solution = pickle.load(f)

existing_sites = load_devon_sites()
existing_sites = existing_sites[existing_sites["Existing"] == "Yes"][
    "Facility_Name"
].to_list()

st.info(
    f"You selected {selected_site} as the best solution.\n\nDoes the optimiser agree?"
)

run = st.button("Click here to run the optimiser")

if run:
    with st.spinner("The optimiser is starting up..."):
        time.sleep(3)

    st.write("The optimiser is evaluating all possible combinations of 5 sites")

    duration = get_gif_duration(gif_path)

    progress = st.progress(0)

    gif_placeholder = st.empty()
    gif_placeholder.image(gif_path)

    for i in range(100):
        time.sleep(duration / 100)
        progress.progress(i + 1)

    best_combo = solution.return_best_combination_site_names()
    best_additional = [i for i in best_combo if i not in existing_sites]

    gif_placeholder.success(
        f"The optimiser finds the best additional site to be {best_additional[0]}."
    )

    solution_df_display = (
        solution.solution_df.copy()
        .drop(columns=["site_indices", "problem_df"])
        .round(2)
    )

    solution_df_display["site"] = solution_df_display["site_names"].apply(
        lambda x: [i for i in x if i not in existing_sites][0]
    )

    solution_df_display = solution_df_display.drop(columns="site_names")

    st.dataframe(
        solution_df_display,
        hide_index=True,
        column_order=[
            "solution_rank",
            "site",
            "weighted_average",
            "unweighted_average",
            "90th_percentile",
            "max",
            "proportion_within_coverage_threshold",
        ],
    )

    st.write("""
    Your solution is the
    -
    -
    -
    -

    """)
