import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Clariflocculator Monitoring",
    layout="wide"
)

# ==================================
# LOAD EXCEL
# ==================================
df = pd.read_excel("Clariflocculator Running Status.xlsx")

# ==================================
# DARK THEME
# ==================================
st.markdown("""
<style>

.stApp{
    background-color:#071425;
}

h1,h2,h3,p,label{
    color:white !important;
}

.status-green{
    color:#00ff66;
    font-weight:bold;
}

.status-red{
    color:#ff3b3b;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# GIF FUNCTION
# ==================================
def show_gif(file_path, width=650):

    with open(file_path, "rb") as f:
        data = f.read()

    data_url = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <div style="text-align:center;">
            data:image/gif;base64,{data_url}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================
# STATUS LOGIC
# ==================================
def get_status(row):

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":

        return {
            "status":"🔴 NOT RUNNING",
            "gif":"assets/clariflocculator_not_running.gif",
            "color":"red"
        }

    else:

        return {
            "status":"🟢 RUNNING",
            "gif":"assets/clariflocculator_running.gif",
            "color":"green"
        }

# ==================================
# HEADER
# ==================================
st.title("💧 CLARIFLOCCULATOR MONITORING")

# ==================================
# KPIs
# ==================================
healthy = 0
alert = 0

for _, row in df.iterrows():

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":
        alert += 1
    else:
        healthy += 1

c1, c2, c3 = st.columns(3)

c1.metric("Total Units", len(df))
c2.metric("Running", healthy)
c3.metric("Not Running", alert)

st.divider()

# ==================================
# VIEW MODE
# ==================================
view_mode = st.radio(
    "View Mode",
    ["Single Location", "Multiple Locations"],
    horizontal=True
)

locations = df["Location"].unique().tolist()

# ==================================
# SINGLE LOCATION
# ==================================
if view_mode == "Single Location":

    selected = st.selectbox(
        "Select Location",
        locations
    )

    row = df[df["Location"] == selected].iloc[0]

    result = get_status(row)

    st.subheader(selected)

    gif_path = Path(result["gif"])

    if gif_path.exists():

        show_gif(gif_path)

    else:

        st.error(
            f"GIF Missing: {gif_path}"
        )

    st.markdown(
        f"## {result['status']}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Bridge Running Status",
            row["Bridge Running Status"]
        )

    with col2:
        st.metric(
            "Blowdown Valve Status",
            row["Blowdown Valve Status"]
        )

# ==================================
# MULTIPLE LOCATION
# ==================================
else:

    selected_locations = st.multiselect(
        "Select Locations",
        locations,
        default=locations
    )

    cols = st.columns(2)

    for i, location in enumerate(selected_locations):

        row = df[df["Location"] == location].iloc[0]

        result = get_status(row)

        with cols[i % 2]:

            st.subheader(location)

            gif_path = Path(result["gif"])

            if gif_path.exists():

                show_gif(
                    gif_path,
                    width=300
                )

            st.markdown(
                f"### {result['status']}"
            )

            st.write(
                "Bridge:",
                row["
