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

# Add in a state ensuring they see at least one demand-related page before unlocking
# the 'make a recommendation' button

# Add in a state ensuring they see at least one ACCESSIBILITY-related page before unlocking
# the 'make a recommendation' button


pg = st.navigation(
    [
        st.Page("app/Homepage.py", title="Welcome!", icon=":material/add_circle:"),
        st.Page("app/Demand.py", title="Where is our demand?"),
        st.Page("app/Deprivation.py", title="Where is there high need?"),
        st.Page("app/Demand_Deprivation_Hotspots.py", title="How do these interact?"),
        st.Page("app/Travel.py", title="What does travel look like now?"),
        st.Page(
            "app/Catchment_Isochrones.py", title="Who is currently underserved?"
        ),  # Isochrones
        st.Page(
            "app/Catchment_2sfca.py", title="Who is currently underserved?"
        ),  # 2sfca
        st.Page("app/Decide.py", title="What's your Decision?"),
        st.Page("app/Optimize.py", title="What does the maths say?"),
        st.Page("app/Compare.py", title="What's the payoff?"),
    ]
)

pg.run()
