import streamlit as st
import pandas as pd
from pathlib import Path
import base64

st.set_page_config(
    page_title="Clariflocculator Monitoring",
    layout="wide"
)

# ===============================
# LOAD EXCEL
# ===============================
df = pd.read_excel("Clariflocculator Running Status.xlsx")

# ===============================
# PAGE STYLE
# ===============================
st.markdown("""
<style>
.stApp {
    background-color: #071425;
    color: white;
}
h1,h2,h3,label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# GIF DISPLAY FUNCTION
# ===============================
def display_gif(gif_path):

    if not Path(gif_path).exists():
        st.error(f"GIF not found: {gif_path}")
        return

    with open(gif_path, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    html = f"""
    <div style="text-align:center;">
        data:image/gif;base64,{encoded}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


# ===============================
# STATUS FUNCTION
# ===============================
def get_status(row):

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":

        return (
            "🔴 NOT RUNNING",
            "assets/clariflocculator_not_running.gif"
        )

    return (
        "🟢 RUNNING",
        "assets/clariflocculator_running.gif"
    )


# ===============================
# HEADER
# ===============================
st.title("💧 Clariflocculator Monitoring Dashboard")

# ===============================
# KPI
# ===============================
running = 0
stopped = 0

for _, row in df.iterrows():

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":
        stopped += 1
    else:
        running += 1

c1, c2, c3 = st.columns(3)

c1.metric("Total Units", len(df))
c2.metric("Running", running)
c3.metric("Stopped", stopped)

st.divider()

# ===============================
# VIEW MODE
# ===============================
view = st.radio(
    "View Mode",
    ["Single Location", "Multiple Locations"],
    horizontal=True
)

locations = list(df["Location"].unique())

# ===============================
# SINGLE LOCATION
# ===============================
if view == "Single Location":

    location = st.selectbox(
        "Select Location",
        locations
    )

    row = df[df["Location"] == location].iloc[0]

    status, gif_path = get_status(row)

    st.subheader(location)

    display_gif(gif_path)

    st.markdown(f"## {status}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Bridge Status",
            row["Bridge Running Status"]
        )

    with col2:
        st.metric(
            "Blowdown Valve Status",
            row["Blowdown Valve Status"]
        )


# ===============================
# MULTIPLE LOCATION
# ===============================
else:

    selected_locations = st.multiselect(
        "Select Locations",
        locations,
        default=locations
    )

    for location in selected_locations:

        row = df[df["Location"] == location].iloc[0]

        status, gif_path = get_status(row)

        st.markdown("---")

        st.subheader(location)

        display_gif(gif_path)

        st.markdown(f"### {status}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Bridge Status",
                row["Bridge Running Status"]
            )

        with col2:
            st.metric(
                "Blowdown Valve Status",
                row["Blowdown Valve Status"]
            )
