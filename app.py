import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Clarifier Monitoring Dashboard",
    layout="wide"
)

# -----------------------------
# SCADA STYLE
# -----------------------------
st.markdown("""
<style>

.stApp{
    background-color:#0B1220;
}

.card{
    background-color:#1a2333;
    padding:15px;
    border-radius:15px;
    text-align:center;
}

.green{
    border:4px solid #00ff88;
    box-shadow:0 0 20px #00ff88;
}

.red{
    border:4px solid red;
    box-shadow:0 0 25px red;
}

.title{
    color:white;
    text-align:center;
}

.value{
    color:white;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD EXCEL
# -----------------------------
df = pd.read_excel("Clariflocculator Running Status.xlsx")

# -----------------------------
# HEALTH LOGIC
# -----------------------------
def unit_status(row):

    if (
        str(row["Bridge Running Status"]).strip() == "Not OK"
        or
        str(row["Blowdown Valve Status"]).strip() == "Not OK"
    ):
        return "🔴 ALERT", "red"

    return "🟢 HEALTHY", "green"

# -----------------------------
# KPI
# -----------------------------
healthy = 0
alert = 0

for _, row in df.iterrows():

    status, _ = unit_status(row)

    if "ALERT" in status:
        alert += 1
    else:
        healthy += 1

st.title("💧 Clarifier & Clariflocculator Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("Total Units", len(df))
c2.metric("Healthy", healthy)
c3.metric("Alert", alert)

st.divider()

# -----------------------------
# UNIT CARD
# -----------------------------
def show_unit(location):

    row = df[df["Location"] == location].iloc[0]

    status, css = unit_status(row)

    st.markdown(
        f"""
        <div class="card {css}">
        <h2 style="color:white;">{location}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        "assets/VN20260821_110432.gif",
        use_container_width=True
    )

    st.markdown(
        f"<h3 style='text-align:center;color:white'>{status}</h3>",
        unsafe_allow_html=True
    )

    st.write(
        f"Bridge : {row['Bridge Running Status']}"
    )

    st.write(
        f"Blowdown : {row['Blowdown Valve Status']}"
    )

    remark = st.selectbox(
        "Remarks",
        [
            "Normal",
            "Greasing Required",
            "Vibration Observed",
            "Valve Leakage",
            "Maintenance Required"
        ],
        key=location
    )

# -----------------------------
# GRID
# -----------------------------
r1c1, r1c2, r1c3 = st.columns(3)

with r1c1:
    show_unit("FH3")

with r1c2:
    show_unit("FH4")

with r1c3:
    show_unit("FH5")

r2c1, r2c2, r2c3 = st.columns(3)

with r2c1:
    show_unit("FH6")

with r2c2:
    show_unit("PART A")

with r2c3:
    show_unit("PART B")
