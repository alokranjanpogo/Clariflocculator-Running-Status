import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title="Clariflocculator Monitoring",
    page_icon="💧",
    layout="wide"
)

# ====================================================
# LOAD EXCEL
# ====================================================

df = pd.read_excel("Clariflocculator Running Status.xlsx")

# ====================================================
# CSS
# ====================================================

st.markdown("""
<style>

.stApp{
    background-color:#071425;
}

h1,h2,h3,h4,p,label{
    color:white !important;
}

.status-ok{
    color:#00ff66;
    font-weight:bold;
}

.status-notok{
    color:red;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ====================================================
# FIND GIFS AUTOMATICALLY
# ====================================================

running_gif = None
not_running_gif = None

for file in Path(".").rglob("*.gif"):

    name = file.name.lower()

    if "running" in name and "not" not in name:
        running_gif = file

    if "not" in name:
        not_running_gif = file

# ====================================================
# GIF DISPLAY
# ====================================================

def show_gif(gif_path):

    if gif_path is None:
        st.error("GIF not found in repository")
        return

    with open(gif_path, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    html = f"""
    <div style="text-align:center;">
        data:image/gif;base64,{encoded}" width="600">
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# ====================================================
# STATUS FUNCTION
# ====================================================

def get_status(row):

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":

        return (
            "🔴 NOT RUNNING",
            not_running_gif
        )

    return (
        "🟢 RUNNING",
        running_gif
    )

# ====================================================
# KPI
# ====================================================

running_count = 0
stopped_count = 0

for _, row in df.iterrows():

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":
        stopped_count += 1
    else:
        running_count += 1

# ====================================================
# HEADER
# ====================================================

st.title("💧 Clariflocculator Monitoring Dashboard")

k1, k2, k3 = st.columns(3)

k1.metric("Total Units", len(df))
k2.metric("Running", running_count)
k3.metric("Not Running", stopped_count)

st.divider()

# ====================================================
# SIDEBAR
# ====================================================

st.sidebar.title("Control Panel")

view_mode = st.sidebar.radio(
    "View Mode",
    [
        "Single Location",
        "Multiple Locations"
    ]
)

locations = sorted(df["Location"].unique())

# ====================================================
# SINGLE LOCATION
# ====================================================

if view_mode == "Single Location":

    selected_location = st.sidebar.selectbox(
        "Select Location",
        locations
    )

    row = df[df["Location"] == selected_location].iloc[0]

    status, gif_path = get_status(row)

    st.subheader(selected_location)

    show_gif(gif_path)

    st.markdown(f"## {status}")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Bridge Status",
            row["Bridge Running Status"]
        )

    with c2:
        st.metric(
            "Blowdown Valve Status",
            row["Blowdown Valve Status"]
        )

# ====================================================
# MULTIPLE LOCATIONS
# ====================================================

else:

    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        locations,
        default=locations
    )

    cols = st.columns(2)

    for i, location in enumerate(selected_locations):

        row = df[df["Location"] == location].iloc[0]

        status, gif_path = get_status(row)

        with cols[i % 2]:

            st.subheader(location)

            show_gif(gif_path)

            st.markdown(f"### {status}")

            st.write(
                "Bridge Status:",
                row["Bridge Running Status"]
            )

            st.write(
                "Blowdown Valve Status:",
                row["Blowdown Valve Status"]
            )

            st.divider()

# ====================================================
# DATA
# ====================================================

with st.expander("Excel Data"):

    st.dataframe(
        df,
        use_container_width=True
    )
