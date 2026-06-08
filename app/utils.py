import pandas as pd
import streamlit as st
import geopandas
import html
from app.utils_investigations import ALL_INVESTIGATIONS, Investigation

TERMINAL_DEFAULT_SPEED = 10
TERMINAL_COLOUR = "yellow"
DECISION_COST = 25
ANALYST_CAPACITY_INITIAL = 100


# Load datasets
@st.cache_data
def load_travel_matrix_car():
    return pd.read_csv("data/devon_miu_travel_matrix.csv")


@st.cache_data
def load_travel_matrix_public():
    return pd.read_csv("data/devon_miu_travel_matrix_public_transport.csv")


@st.cache_data
def load_devon_sites():
    return geopandas.read_file("data/devon_mius.geojson")


@st.cache_data
def load_devon_geography():
    return geopandas.read_file("data/LSOA_Devon_2021_EW_BSC_V4.gpkg")


@st.cache_data
def load_deprivation():
    return pd.read_csv("data/devon_imd_2025_2021_LSOAs.csv")


@st.cache_data
def load_demand():
    return pd.read_csv("data/demand_MF_50_84.csv")


@st.cache_data
def create_demand_gdf():
    devon_gdf = load_devon_geography()
    demand_df = load_demand()
    full_gdf = devon_gdf.merge(demand_df, left_on="LSOA21NM", right_on="LSOA 2021 Name")
    return full_gdf


def write_terminal_html(
    text: str,
    output_path: str = "app/assets/terminal.html",
    colour: str = TERMINAL_COLOUR,
    glow_amount: float = 0.7,
    reveal_speed_ms: int = TERMINAL_DEFAULT_SPEED,
    cursor: str = "block",
    stay_blinking: bool = True,
):
    with open("app/assets/terminal.css") as f:
        css = f.read()
    with open("app/assets/terminal.js") as f:
        js = f.read()

    safe_text = html.escape(text, quote=True)
    strong_pct = int(glow_amount * 100)
    soft_pct = int(glow_amount * 40)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<style>
    {css}
    :root {{
        --terminal-colour: {colour};
        --terminal-glow-strong: color-mix(in srgb, {colour} {strong_pct}%, transparent);
        --terminal-glow-soft: color-mix(in srgb, {colour} {soft_pct}%, transparent);
    }}
</style>
</head>
<body>
  <div id="typewrite" class="typeing" data-text="{safe_text}"></div>
  <script>
    var REVEAL_SPEED_MS = {reveal_speed_ms};
    var CURSOR = {repr(cursor)};
    var STAY_BLINKING = {"true" if stay_blinking else "false"};
    {js}
  </script>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html_content)

    return len(text), reveal_speed_ms


def record_page_visited(investigation: Investigation) -> None:
    """Record a visit to an investigation page by ID."""
    visited_ids = [v["id"] for v in st.session_state.pages_visited]
    if investigation.id not in visited_ids:
        step = len(st.session_state.pages_visited) + 1
        st.session_state.pages_visited.append(
            {
                "step": step,
                "id": investigation.id,
                "title": investigation.title,
                "analyst_days": investigation.analyst_days,
            }
        )


def _prerequisites_met(investigation: Investigation) -> bool:
    visited_ids = {v["id"] for v in st.session_state.pages_visited}
    return all(p in visited_ids for p in investigation.prerequisites)


def _already_visited(investigation: Investigation) -> bool:
    visited_ids = {v["id"] for v in st.session_state.pages_visited}
    return investigation.id in visited_ids


def investigation_button(investigation: Investigation) -> None:
    """
    Render a single investigation button.

    - Hidden if prerequisites are unmet.
    - Greyed out (non-clickable) if already visited.
    - Active and clickable otherwise.
    """
    if not _prerequisites_met(investigation):
        return  # Hidden entirely

    visited = _already_visited(investigation)
    button_key = f"inv_btn_{investigation.id}"

    # Lucide icon via CDN — swap icon name to any at lucide.dev/icons
    icon_html = f"""
        <script src="https://unpkg.com/lucide@latest"></script>
        <i data-lucide="{investigation.icon}"
           style="width:18px;height:18px;stroke-width:1.75;vertical-align:middle;
                  margin-right:8px;{"opacity:0.4;" if visited else ""}">
        </i>
        <script>lucide.createIcons();</script>
    """

    if visited:
        # Render as static greyed-out tile — no button interaction
        st.html(f"""
            <div style="
                display: flex;
                align-items: center;
                padding: 12px 16px;
                border-radius: 8px;
                border: 1.5px solid #e0e0e0;
                background: #f7f7f7;
                color: #aaa;
                font-size: 0.92rem;
                cursor: not-allowed;
                margin-bottom: 6px;
                user-select: none;
            ">
                {icon_html}
                <span>✓ {investigation.analyst_prompt}</span>
            </div>
        """)
    else:
        # Use a real Streamlit button for click handling
        col_icon, col_text = st.columns([0.08, 0.92])
        with col_icon:
            st.html(icon_html)
        with col_text:
            if st.button(
                investigation.analyst_prompt,
                key=button_key,
                use_container_width=True,
            ):
                record_page_visited(investigation)
                st.switch_page(investigation.page)


# components/investigation_button.py (addition)


def render_navigation(current: Investigation) -> None:
    """
    Render the full navigation section for a given investigation page.
    Call once at the bottom of each page after content.
    """
    st.subheader("Recommended next steps")
    for inv_id in current.recommended_next:
        if inv_id in ALL_INVESTIGATIONS:
            investigation_button(ALL_INVESTIGATIONS[inv_id])

    other_investigations = [
        inv
        for inv_id, inv in ALL_INVESTIGATIONS.items()
        if inv_id not in set(current.recommended_next) | {current.id}
    ]

    if any(
        _prerequisites_met(inv) and not _already_visited(inv)
        for inv in other_investigations
    ):
        st.divider()
        st.subheader("Other available investigations")
        for inv in other_investigations:
            investigation_button(inv)
