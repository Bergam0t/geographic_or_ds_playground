import streamlit as st

states = [
    "catchment_page_visited",
    "compare_page_visited",
    "demand_deprivation_hotspots_page_visited",
    "demand_page_visited",
    "deprivation_page_visited",
    "homepage_visited",
    "optimize_page_visited",
    "travel_page_visited",
]

for state in states:
    if state not in st.session_state:
        st.session_state[state] = False

if "pages_visited" not in st.session_state:
    st.session_state.pages_visited = []

if "homepage_visited" not in st.session_state:
    st.session_state.homepage_visited = False

# Add in a state ensuring they see at least one DEMAND-related page before unlocking
# the 'make a recommendation' button
if "observed_one_demand_page" not in st.session_state:
    st.session_state.observed_one_demand_page = False

# Add in a state ensuring they see at least one ACCESSIBILITY-related page before unlocking
# the 'make a recommendation' button
if "observed_one_accessibility_page" not in st.session_state:
    st.session_state.observed_one_accessibility_page = False

pg = st.navigation(
    [
        st.Page("app/Homepage.py", title="Welcome!"),
        st.Page("app/Demand.py", title="Where is our demand?"),
        st.Page("app/Deprivation.py", title="Where is there high need?"),
        st.Page("app/Demand_Hotspots.py", title="Where is demand concentrated?"),
        st.Page(
            "app/Deprivation_Hotspots.py", title="Where is deprivation concentrated?"
        ),
        st.Page(
            "app/Demand_Deprivation_Hotspots.py",
            title="Where do areas of both high demand and high deprivation occur?",
        ),
        # Transport pages without cross-border travel to nearest CDCs
        st.Page("app/Travel_Car.py", title="What does travel by car look like now?"),
        st.Page(
            "app/Travel_Public_Transport.py",
            title="What does travel by public transport look like now?",
        ),
        st.Page(
            "app/Deprivation_Travel_Hotspots.py",
            title="Where do high deprivation and high travel times intersect?",
        ),
        st.Page(
            "app/Demand_Travel_Hotspots.py",
            title="Where do high demand and high travel times intersect?",
        ),
        # Isochrones as a visual way of exploring travel time
        st.Page(
            "app/Catchment_Isochrones_car.py",
            title="Where are the transport gaps by car?",
        ),
        st.Page(
            "app/Catchment_Isochrones_pt.py",
            title="Where are the transport gaps by public tranport?",
        ),
        # 2 step floating catchment area - again, what to do about car vs PT, and cross-border?
        st.Page("app/Catchment_2sfca_car.py", title="Who is currently underserved?"),
        # 2 step floating catchment area - again, what to do about car vs PT, and cross-border?
        st.Page("app/Catchment_2sfca_pt.py", title="Who is currently underserved?"),
        # This page will have a summary of all of the information they have uniquely collected.
        # Buttons will lead out to 'Collect More Evidence' or
        st.Page("app/Running_Evidence_Summary.py", title="What do we know so far?"),
        # Explore the utilisation of existing CDCs (capacity vs catchment)
        st.Page("app/Utilisation.py", title="What's your Decision?"),
        # Display projected demand
        st.Page("app/Projected_Demand.py", title="What's your Decision?"),
        # NOTE - DO WE NEED PROJECTED UTILISATION TOO?
        # This page will also have a summary of all of the information they have uniquely collected.
        st.Page("app/Decide.py", title="What's your Decision?"),
        # Next, we go to the optimization page.
        st.Page("app/Optimize.py", title="What does the maths say?"),
        # We can compare both their solution and the optimized solution against the existing solution to show
        # the benefits and who they affect
        st.Page("app/Compare.py", title="What's the payoff?"),
    ]
)

pg.run()
