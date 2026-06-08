import streamlit as st

states = ["homepage_visited"]

for state in states:
    if state not in st.session_state:
        st.session_state[state] = False

pg = st.navigation(
    [
        st.Page("app/Homepage.py", title="Welcome!", icon=":material/add_circle:"),
        st.Page("app/Demand.py", title="Where is our demand?"),
        st.Page("app/Deprivation.py", title="Where is there high need?"),
        st.Page("app/Demand_Deprivation_Hotspots.py", title="How do these interact?"),
        st.Page("app/Travel.py", title="What does travel look like now?"),
        st.Page(
            "app/Catchment.py", title="Who is currently underserved?"
        ),  # Isochrones, 2sfca
        st.Page("app/Optimize.py", title="Where should we put an extra site?"),
        st.Page("app/Compare.py", title="What's the payoff?"),
    ]
)

pg.run()
