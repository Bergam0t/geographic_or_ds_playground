from dataclasses import dataclass


@dataclass
class Investigation:
    id: str
    title: str
    page: str

    category: str

    prerequisites: list[str]
    parent: str | None

    analyst_prompt: str

    recommended_next: list[str]
    is_entry_point: bool


DEMAND = Investigation(
    id="demand",
    title="Where is our demand?",
    page="app/Demand.py",
    category="need",
    prerequisites=[],
    parent=None,
    recommended_next=[
        "deprivation",
        "hotspots",
        "travel_car",
    ],
    analyst_prompt=("Map the population aged 50-85 who may require CDC services."),
    is_entry_point=True,
)

DEPRIVATION = Investigation(
    id="deprivation",
    title="Where is there high need?",
    page="app/Deprivation.py",
    category="equity",
    prerequisites=[],
    parent=None,
    recommended_next=[
        "hotspots",
        "demand",
        "travel_car",
    ],
    analyst_prompt=("Show me areas experiencing the highest deprivation."),
    is_entry_point=True,
)

TRAVEL_CAR = Investigation(
    id="travel_car",
    title="Travel by car",
    page="app/Travel_Car.py",
    category="accessibility",
    prerequisites=[],
    parent=None,
    recommended_next=[
        "travel_car_cross_border",
        "travel_pt",
        "isochrones",
        "2sfca",
    ],
    analyst_prompt=("Show travel times to existing CDCs."),
    is_entry_point=True,
)

TRAVEL_CAR_ADVANCED = Investigation(
    id="travel_car_cross_border",
    title="Investigate boundary effects",
    page="app/Travel_Car_Advanced.py",
    category="accessibility",
    prerequisites=["travel_car"],
    parent="travel_car",
    recommended_next=[
        "travel_pt",
        "travel_both_cross_border",
        "isochrones",
    ],
    analyst_prompt=("Include CDCs outside Devon when calculating travel times."),
    is_entry_point=False,
)

TRAVEL_PT = Investigation(
    id="travel_pt",
    title="Travel by public transport",
    page="app/Travel_Public_Transport.py",
    category="accessibility",
    prerequisites=[],
    parent="travel_car",
    recommended_next=[
        "travel_pt_cross_border",
        "travel_both_cross_border",
        "isochrones",
    ],
    analyst_prompt=(
        "Look at how travel times are different if patients are using public transport."
    ),
    is_entry_point=False,
)

TRAVEL_PT_ADVANCED = Investigation(
    id="travel_pt_cross_border",
    title="Public transport with neighbouring CDCs",
    page="app/Travel_Public_Transport_Advanced.py",
    category="accessibility",
    prerequisites=["travel_pt"],
    parent="travel_pt",
    recommended_next=[
        "travel_both_cross_border",
        "isochrones",
    ],
    analyst_prompt=("Consider both public transport and neighbouring CDCs."),
    is_entry_point=False,
)

TRAVEL_BOTH_ADVANCED = Investigation(
    id="travel_both_cross_border",
    title="Combined accessibility assessment",
    page="app/Travel_Both_Advanced.py",
    category="accessibility",
    prerequisites=[
        "travel_car_cross_border",
        "travel_pt_cross_border",
    ],
    parent=None,
    recommended_next=[
        "isochrones",
        "hotspots",
    ],
    analyst_prompt=("Compare accessibility using multiple travel modes."),
    is_entry_point=False,
)

HOTSPOTS_DEMAND = Investigation(
    id="hotspots",
    title="Demand hotspots",
    page="app/Demand_Hotspots.py",
    category="need",
    prerequisites=[
        "demand",
    ],
    parent=None,
    analyst_prompt=("Identify clusters of demand."),
    is_entry_point=False,
)

HOTSPOTS_DEPRIVATION = Investigation(
    id="hotspots_deprivation",
    title="Deprivation hotspots",
    page="app/Deprivation_Hotspots.py",
    category="equity",
    prerequisites=[
        "deprivation",
    ],
    recommended_next=["travel_time_car"],
    parent=None,
    analyst_prompt=("Identify clusters of deprivation."),
    is_entry_point=False,
)

HOTSPOTS_DEMAND_DEPRIVATION = Investigation(
    id="hotspots_combined",
    title="Demand and deprivation hotspots",
    page="app/Demand_Deprivation_Hotspots.py",
    category="need",
    prerequisites=[
        "demand",
        "deprivation",
    ],
    parent=None,
    analyst_prompt=("Combine demand and deprivation to identify priority areas."),
    is_entry_point=False,
)

ISOCHRONES = Investigation(
    id="isochrones",
    title="Catchment areas",
    page="app/Catchment_Isochrones.py",
    category="accessibility",
    prerequisites=[],
    parent="travel_car",
    recommended_next=[
        "2sfca",
    ],
    analyst_prompt=("Show which communities fall within key travel-time thresholds."),
    is_entry_point=False,
)

# Note that when we get to that page we can just use whatever travel data exists?
# if "travel_pt" in visited:
#     use_pt_isochrones()
# elif "travel_car_cross_border" in visited:
#     use_cross_border_isochrones()
# else:
#     use_car_isochrones()

TWO_SFCA = Investigation(
    id="2sfca",
    title="Service availability",
    page="app/Catchment_2sfca.py",
    category="accessibility",
    prerequisites=["isochrones"],
    parent="isochrones",
    recommended_next=[
        "hotspots",
        "decision",
    ],
    analyst_prompt=("Calculate the 2 step floating catchment area metric."),
    is_entry_point=False,
)

UTILISATION = Investigation(
    id="utilisation",
    title="How well-used are existing CDCs?",
    page="app/Utilisation.py",
    category="capacity",
    prerequisites=[],
    parent=None,
    is_entry_point=False,
    recommended_next=[
        "demand",
    ],
    analyst_prompt="Show me how well-used the existing four CDCs are.",
)

PROJECTED_DEMAND = Investigation(
    id="projected_demand",
    title="Where will demand be in the future?",
    page="app/Projected_Demand.py",
    category="demand",
    prerequisites=[
        "demand",
    ],
    parent="demand",
    is_entry_point=False,
    recommended_next=[
        "hotspots",
        "hotspots_combined",
        "deprivation",
    ],
    analyst_prompt="Show me how the 50-85 population is projected to change across Devon in the next 10 years.",
)
