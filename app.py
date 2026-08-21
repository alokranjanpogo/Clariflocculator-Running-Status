import streamlit as st
import pandas as pd
from pathlib import Path

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="Clariflocculator Dashboard",
    page_icon="💧",
    layout="wide"
)

# ------------------------
# LOAD DATA
# ------------------------
df = pd.read_excel("Clariflocculator Running Status.xlsx")

# ------------------------
# CSS
# ------------------------
st.markdown("""
<style>

.stApp{
    background-color:#071425;
}

.block-container{
    padding-top:1rem;
}

.title{
    text-align:center;
    color:white;
    font-size:36px;
    font-weight:bold;
}

.info-box{
    background:#0f2740;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# STATUS FUNCTION
# ------------------------
def get_status(row):

    bridge = str(row["Bridge Running Status"]).strip()
    blowdown = str(row["Blowdown Valve Status"]).strip()

    if bridge == "Not OK" or blowdown == "Not OK":
        return (
            "NOT RUNNING",
            "red",
            "assets/clariflocculator_not_running.gif"
        )

    return (
        "RUNNING",
        "lime",
        "assets/clariflocculator_running.gif"
    )

# ------------------------
# HEADER
# ------------------------
st.markdown(
    "<h1 class='title'>CLARIFLOCCULATOR MONITORING</h1>",
    unsafe_allow_html=True
)

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.header("Selection")

mode = st.sidebar.radio(
    "View Mode",
    [
        "Single Location",
        "Multiple Locations"
    ]
)

locations = list(df["Location"].unique())

# ======================================================
# SINGLE LOCATION
# ======================================================

if mode == "Single Location":

    selected = st.sidebar.selectbox(
        "Select Location",
        locations
    )

    row = df[df["Location"] == selected].iloc[0]

    status, color, gif_path = get_status(row)

    st.subheader(selected)

    if Path(gif_path).exists():

        with open(gif_path, "rb") as file:
            gif = file.read()

        st.image(
            gif,
            width=650
        )

    else:
        st.error(f"GIF Not Found: {gif_path}")

    st.markdown(
        f"<h2 style='color:{color};'>{status}</h2>",
        unsafe_allow_html=True
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

    st.markdown("---")

    problem = st.selectbox(
        "Problem",
        [
            "No Problem",
            "Bridge Jam",
            "Motor Fault",
            "Gearbox Issue",
            "Valve Leakage",
            "Electrical Fault"
        ]
    )

    remarks = st.text_area(
        "Remarks",
        "Enter Remarks Here"
    )

    st.success(f"Problem: {problem}")
    st.info(f"Remarks: {remarks}")

# ======================================================
# MULTI LOCATION
# ======================================================

else:

    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        locations,
        default=locations[:2]
    )

    cols = st.columns(2)

    for i, location in enumerate(selected_locations):

        row = df[df["Location"] == location].iloc[0]

        status, color, gif_path = get_status(row)

        with cols[i % 2]:

            st.subheader(location)

            if Path(gif_path).exists():

                with open(gif_path, "rb") as file:
                    gif = file.read()

                st.image(
                    gif,
                    width=350
                )

            st.markdown(
                f"""
                <h3 style='color:{color};'>
                {status}
                </h3>
                """,
                unsafe_allow_html=True
            )

            st.write(
                f"Bridge: {row['Bridge Running Status']}"
            )

            st.write(
                f"Blowdown: {row['Blowdown Valve Status']}"
            )

            problem = st.selectbox(
                f"Problem - {location}",
                [
                    "No Problem",
                    "Bridge Jam",
                    "Motor Fault",
                    "Gearbox Issue",
                    "Valve Leakage",
                    "Electrical Fault"
                ],
                key=f"problem_{location}"
            )

            remarks = st.text_input(
                f"Remarks - {location}",
                key=f"remark_{location}"
            )

            st.divider()

# ------------------------
# DATA TABLE
# ------------------------
with st.expander("View Data"):

    st.dataframe(
        df,
        use_container_width=True
    )
