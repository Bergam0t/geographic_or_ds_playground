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

if "nav_history" not in st.session_state:
    st.session_state.nav_history = []

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
        st.Page("app/Homepage.py", title="Welcome!", icon=":material/add_circle:"),
        st.Page("app/Demand.py", title="Where is our demand?"),
        st.Page("app/Deprivation.py", title="Where is there high need?"),
        st.Page("app/Demand_Deprivation_Hotspots.py", title="How do these interact?"),
        # Transport pages without cross-border travel to nearest CDCs
        st.Page("app/Travel_Car.py", title="What does travel by car look like now?"),
        st.Page(
            "app/Travel_Public_Transport.py",
            title="What does travel by public transport look like now?",
        ),
        # Can get to this one by first doing car
        st.Page(
            "app/Travel_Car_Advanced.py", title="What does travel by car look like now?"
        ),
        # Can get to this one by first doing public transport
        st.Page(
            "app/Travel_Public_Transport_Advanced.py",
            title="What does travel by public transport look like now if we include cross-border travel?",
        ),
        # Can only do this one if both car and public transport previously chosen but are now
        # wanting to add cross-border CDCs
        st.Page(
            "app/Travel_Both_Advanced.py",
            title="What does travel by car and public transport look like now  if we include cross-border travel?",
        ),
        # Isochrones as a visual way of exploring travel time
        # NOTE: do we need separate car and public transport again? Do the different options open up
        # depending on what they've chosen in terms of general travel time choropleths previously?
        # Or do these isochrones need their own variant pages?
        st.Page(
            "app/Catchment_Isochrones.py", title="Who is currently underserved?"
        ),  # 2 step floating catchment area - again, what to do about car vs PT, and cross-border?
        st.Page("app/Catchment_2sfca.py", title="Who is currently underserved?"),
        # This page will have a summary of all of the information they have uniquely collected.
        # Buttons will lead out to 'Collect More Evidence' or
        st.Page("app/Running_Evidence_Summary.py", title="What do we know so far?"),
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
