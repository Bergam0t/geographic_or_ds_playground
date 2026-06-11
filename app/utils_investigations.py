from dataclasses import dataclass


@dataclass
class Investigation:
    id: str
    title: str
    page: str

    category: list[str]

    prerequisites: list[str]
    parent: str | None

    analyst_prompt: str

    recommended_next: list[str]
    is_entry_point: bool

    analyst_days: float
    icon: str = "arrow_forward"


DEMAND = Investigation(
    id="demand",
    title="Where is our demand?",
    page="app/Demand.py",
    category=["need"],
    prerequisites=[],
    parent=None,
    recommended_next=[
        "deprivation",
        "hotspots_demand",
        "travel_car",
    ],
    analyst_prompt=("Show me the population aged 50-85 who may require CDC services."),
    is_entry_point=True,
    analyst_days=0.5,
    icon="groups_2",
)

DEPRIVATION = Investigation(
    id="deprivation",
    title="Where is there high need?",
    page="app/Deprivation.py",
    category=["equity"],
    prerequisites=[],
    parent=None,
    recommended_next=[
        "hotspots_deprivation",
        "demand",
        "hotspots_demand",
        "travel_car",
    ],
    analyst_prompt=("Show me areas experiencing the highest deprivation."),
    is_entry_point=True,
    analyst_days=0.5,
    icon="payment_arrow_down",
)

TRAVEL_CAR = Investigation(
    id="travel_car",
    title="Travel by car",
    page="app/Travel_Car.py",
    category=["accessibility"],
    prerequisites=[],
    parent=None,
    recommended_next=["travel_pt", "isochrones_car", "demand"],
    analyst_prompt=("Show me travel times to existing CDCs."),
    is_entry_point=True,
    analyst_days=3,
    icon="directions_car",
)

TRAVEL_PT = Investigation(
    id="travel_pt",
    title="Travel by public transport",
    page="app/Travel_Public_Transport.py",
    category=["accessibility"],
    prerequisites=[],
    parent="travel_car",
    recommended_next=["isochrones_pt", "travel_car", "demand"],
    analyst_prompt=(
        "Look at how travel times are different if patients are using public transport."
    ),
    is_entry_point=False,
    analyst_days=5,
)

HOTSPOTS_DEMAND = Investigation(
    id="hotspots_demand",
    title="Demand hotspots",
    page="app/Demand_Hotspots.py",
    category=["need"],
    prerequisites=[
        "demand",
    ],
    parent=None,
    recommended_next=[
        "deprivation",
        "hotspots_deprivation",
        "hotspots_demand_deprivation",
    ],
    analyst_prompt=("Identify clusters of demand."),
    is_entry_point=False,
    analyst_days=1,
)

HOTSPOTS_DEPRIVATION = Investigation(
    id="hotspots_deprivation",
    title="Deprivation hotspots",
    page="app/Deprivation_Hotspots.py",
    category=["equity"],
    prerequisites=[
        "deprivation",
    ],
    recommended_next=["demand", "hotspots_demand", "hotspots_demand_deprivation"],
    parent=None,
    analyst_prompt=("Identify clusters of deprivation."),
    is_entry_point=False,
    analyst_days=1,
)

HOTSPOTS_DEMAND_DEPRIVATION = Investigation(
    id="hotspots_combined",
    title="Demand and deprivation hotspots",
    page="app/Demand_Deprivation_Hotspots.py",
    category=["need", "equity"],
    prerequisites=[
        "demand",
        "deprivation",
    ],
    recommended_next=[
        "travel_car",
        "travel_pt",
        "hotspots_demand_travel",
        "hotspots_deprivation_travel",
    ],
    parent=None,
    analyst_prompt=("Combine demand and deprivation to identify priority areas."),
    is_entry_point=False,
    analyst_days=1,
)

HOTSPOTS_DEMAND_TRAVEL = Investigation(
    id="hotspots_demand_travel",
    title="Demand and travel hotspots",
    page="app/Demand_Travel_Hotspots.py",
    category=["need", "accessibility"],
    # We'll probably just make this only look at car travel
    # as adding pt prerequisite is a bit harsh
    prerequisites=[
        "demand",
        "travel_car",
    ],
    recommended_next=["hotspots_deprivation", "hotspots_deprivation_travel"],
    parent=None,
    analyst_prompt=(
        "Combine demand and travel time to explore hotspots of poor access for high demand areas."
    ),
    is_entry_point=False,
    analyst_days=1,
)

HOTSPOTS_DEPRIVATION_TRAVEL = Investigation(
    id="hotspots_deprivation_travel",
    title="Deprivation and Travel Hotspots",
    page="app/Deprivation_Travel_Hotspots.py",
    category=["equity", "accessibility"],
    # We'll probably just make this only look at car travel
    # as adding pt prerequisite is a bit harsh
    prerequisites=["deprivation", "travel_car"],
    recommended_next=["hotspots_demand_travel"],
    parent=None,
    analyst_prompt=(
        "Combine deprivation and travel time to explore hotspots of poor access for deprived communities."
    ),
    is_entry_point=False,
    analyst_days=1,
)

ISOCHRONES_CAR = Investigation(
    id="isochrones_car",
    title="Catchment Areas - Car",
    page="app/Catchment_Isochrones_car.py",
    category=["accessibility"],
    prerequisites=["travel_car"],
    parent="travel_car",
    recommended_next=["2sfca_car", "travel_pt", "isochrones_pt"],
    analyst_prompt=(
        "Show which communities fall within key travel-time thresholds by car."
    ),
    is_entry_point=False,
    analyst_days=2,
)

ISOCHRONES_PT = Investigation(
    id="isochrones_pt",
    title="Catchment Areas - Public Transport",
    page="app/Catchment_Isochrones_pt.py",
    category=["accessibility"],
    prerequisites=["travel_pt"],
    parent="travel_pt",
    recommended_next=["2sfca_pt", "travel_car", "isochrones_car"],
    analyst_prompt=(
        "Show which communities fall within key travel-time thresholds by public transport."
    ),
    is_entry_point=False,
    analyst_days=2,
)

TWO_SFCA_CAR = Investigation(
    id="2sfca_car",
    title="Service availability - car",
    page="app/Catchment_2sfca_car.py",
    category=["accessibility"],
    prerequisites=["isochrones_car"],
    parent="isochrones_car",
    recommended_next=["hotspots_demand", "travel_pt", "isochrones_pt", "2sfca_pt"],
    analyst_prompt=(
        "Calculate the 2 step floating catchment area metric for car transport."
    ),
    is_entry_point=False,
    analyst_days=2,
)

TWO_SFCA_PT = Investigation(
    id="2sfca_pt",
    title="Service availability - public transport",
    page="app/Catchment_2sfca_pt.py",
    category=["accessibility"],
    prerequisites=["isochrones_pt"],
    parent="isochrones_pt",
    recommended_next=["hotspots_demand", "travel_car", "isochrones_car", "2sfca_car"],
    analyst_prompt=(
        "Calculate the 2 step floating catchment area metric for public transport."
    ),
    is_entry_point=False,
    analyst_days=2,
)

UTILISATION = Investigation(
    id="utilisation",
    title="How well-used are existing CDCs?",
    page="app/Utilisation.py",
    category=["capacity"],
    prerequisites=[],
    parent=None,
    is_entry_point=False,
    recommended_next=["demand", "projected_demand", "travel_car"],
    analyst_prompt="Show me how well-used the existing four CDCs are.",
    analyst_days=2,
)

PROJECTED_DEMAND = Investigation(
    id="projected_demand",
    title="Where will demand be in the future?",
    page="app/Projected_Demand.py",
    category=["need"],
    prerequisites=[
        "demand",
    ],
    parent="demand",
    is_entry_point=False,
    recommended_next=[
        "hotspots_demand",
        "hotspots_combined",
        "deprivation",
        "utilisation",
        "travel_car",
    ],
    analyst_prompt="Show me how the 50-85 population is projected to change across Devon in the next 10 years.",
    analyst_days=2,
)

# At the bottom of investigations.py

ALL_INVESTIGATIONS: dict[str, Investigation] = {
    inv.id: inv
    for inv in [
        DEMAND,
        DEPRIVATION,
        TRAVEL_CAR,
        TRAVEL_PT,
        HOTSPOTS_DEMAND,
        HOTSPOTS_DEPRIVATION,
        HOTSPOTS_DEMAND_DEPRIVATION,
        HOTSPOTS_DEMAND_TRAVEL,
        HOTSPOTS_DEPRIVATION_TRAVEL,
        ISOCHRONES_CAR,
        ISOCHRONES_PT,
        TWO_SFCA_CAR,
        TWO_SFCA_PT,
        UTILISATION,
        PROJECTED_DEMAND,
    ]
}
