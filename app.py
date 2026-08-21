import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Clariflocculator Dashboard",
    page_icon="💧",
    layout="wide"
)

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>

.stApp{
    background-color:#0B1220;
}

.main-title{
    text-align:center;
    color:white;
    font-size:40px;
    font-weight:bold;
}

.unit-card{
    background-color:#1F2937;
    border-radius:15px;
    padding:15px;
}

.metric-container{
    background-color:#1F2937;
    padding:10px;
    border-radius:10px;
}

.footer-text{
    color:white;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# LOAD EXCEL
# -----------------------

df = pd.read_excel(
    "Clariflocculator Running Status.xlsx"
)

# -----------------------
# STATUS FUNCTION
# -----------------------

def get_status(row):

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":
        return "🔴 ALERT", "red"

    return "🟢 HEALTHY", "green"


# -----------------------
# KPI
# -----------------------

healthy = 0
alert = 0

for _, row in df.iterrows():

    status, color = get_status(row)

    if "ALERT" in status:
        alert += 1
    else:
        healthy += 1

# -----------------------
# HEADER
# -----------------------

st.markdown(
    '<p class="main-title">💧 Clarifier & Clariflocculator Dashboard</p>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

c1.metric("Total Units", len(df))
c2.metric("Healthy", healthy)
c3.metric("Alert", alert)

st.divider()

# -----------------------
# SIDEBAR
# -----------------------

st.sidebar.title("Filters")

locations = list(df["Location"].unique())

view_mode = st.sidebar.radio(
    "View Mode",
    [
        "Single Location",
        "Multiple Locations"
    ]
)

# -----------------------
# GIF PATH
# -----------------------

gif_path = (
    Path(__file__).parent
    / "assets"
    / "VN20260821_110432.gif"
)

# -----------------------
# UNIT DISPLAY
# -----------------------

def show_unit(location):

    row = df[df["Location"] == location].iloc[0]

    status, color = get_status(row)

    if color == "green":
        border = "#00ff88"
    else:
        border = "#ff3131"

    st.markdown(
        f"""
        <div style="
        border:4px solid {border};
        padding:15px;
        border-radius:15px;
        background:#1F2937;">
        <h2 style="color:white;text-align:center;">
        {location}
        </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    if gif_path.exists():

        try:
            with open(gif_path, "rb") as file:
                gif = file.read()

            st.image(
                gif,
                use_container_width=True
            )

        except Exception as e:
            st.warning(f"GIF Error: {e}")

    else:
        st.warning("GIF not found")

    st.markdown(
        f"""
        <h3 style="
        color:{border};
        text-align:center;">
        {status}
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write(
        f"**Bridge Status:** {row['Bridge Running Status']}"
    )

    st.write(
        f"**Blowdown Valve Status:** {row['Blowdown Valve Status']}"
    )

    remark = st.selectbox(
        f"Remarks - {location}",
        [
            "Normal",
            "Greasing Required",
            "Valve Leakage",
            "Maintenance Required",
            "Vibration Observed",
            "Inspection Planned"
        ],
        key=f"remark_{location}"
    )

    st.info(f"Selected Remark: {remark}")


# -----------------------
# SINGLE LOCATION VIEW
# -----------------------

if view_mode == "Single Location":

    selected_location = st.sidebar.selectbox(
        "Select Location",
        locations
    )

    show_unit(selected_location)

# -----------------------
# MULTI LOCATION VIEW
# -----------------------

else:

    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        locations,
        default=locations
    )

    cols = st.columns(3)

    for i, location in enumerate(selected_locations):

        with cols[i % 3]:

            show_unit(location)

# -----------------------
# RAW DATA
# -----------------------

with st.expander("View Excel Data"):

    st.dataframe(
        df,
        use_container_width=True
    )

# -----------------------
# FOOTER
# -----------------------

st.divider()

st.markdown(
    """
    <p class="footer-text">
    Developed for Clarifier & Clariflocculator Monitoring
    </p>
    """,
    unsafe_allow_html=True
)
