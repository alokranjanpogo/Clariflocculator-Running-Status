import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Clariflocculator SCADA",
    layout="wide"
)

# =====================
# LOAD EXCEL
# =====================

df = pd.read_excel(
    "Clariflocculator Running Status.xlsx"
)

# =====================
# CSS
# =====================

st.markdown("""
<style>

.stApp{
    background:#f4f6f8;
}

.scada-box{
    background:white;
    border-radius:15px;
    padding:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.15);
}

.running-light{
    width:20px;
    height:20px;
    background:#00cc44;
    border-radius:50%;
    display:inline-block;
    box-shadow:0 0 20px #00cc44;
}

.stop-light{
    width:20px;
    height:20px;
    background:red;
    border-radius:50%;
    display:inline-block;
    box-shadow:0 0 20px red;
}

.clarifier{
    position:relative;
    width:250px;
    height:250px;
    border:8px solid #3A7BD5;
    border-radius:50%;
    margin:auto;
    background:#dfefff;
}

.bridge{
    position:absolute;
    top:50%;
    left:50%;
    width:180px;
    height:6px;
    background:#444;
    transform-origin:center center;
}

.rotate{
    animation:spin 8s linear infinite;
}

.stop{
    transform:translate(-50%,-50%);
}

.rotate{
    transform:translate(-50%,-50%);
}

@keyframes spin{

    from{
        transform:translate(-50%,-50%) rotate(0deg);
    }

    to{
        transform:translate(-50%,-50%) rotate(360deg);
    }
}

.status-text{
    text-align:center;
    font-size:24px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================
# STATUS LOGIC
# =====================

def get_status(row):

    bridge = str(
        row["Bridge Running Status"]
    ).strip()

    blowdown = str(
        row["Blowdown Valve Status"]
    ).strip()

    if bridge == "Not OK" or blowdown == "Not OK":

        return {
            "running":False,
            "status":"🔴 NOT RUNNING"
        }

    return {
        "running":True,
        "status":"🟢 RUNNING"
    }

# =====================
# HEADER
# =====================

st.title(
    "💧 Clarifier / Clariflocculator SCADA"
)

# =====================
# KPI
# =====================

running_count = 0
stop_count = 0

for _, row in df.iterrows():

    result = get_status(row)

    if result["running"]:
        running_count += 1
    else:
        stop_count += 1

c1,c2,c3 = st.columns(3)

c1.metric(
    "Total Units",
    len(df)
)

c2.metric(
    "Running",
    running_count
)

c3.metric(
    "Not Running",
    stop_count
)

# =====================
# SIDEBAR
# =====================

st.sidebar.title("Control Panel")

view_mode = st.sidebar.radio(
    "View Mode",
    [
        "Single Location",
        "Multiple Locations"
    ]
)

locations = list(
    df["Location"].unique()
)

# =====================
# DRAW UNIT
# =====================

def draw_unit(location):

    row = df[
        df["Location"] == location
    ].iloc[0]

    result = get_status(row)

    if result["running"]:

        light = "running-light"
        bridge_class = "bridge rotate"

    else:

        light = "stop-light"
        bridge_class = "bridge stop"

    st.markdown(
        f"""
        <div class="scada-box">

        <h2 style="text-align:center;">
        {location}
        </h2>

        <div class="clarifier">

            <div class="{bridge_class}">
            </div>

        </div>

        <br>

        <div style="text-align:center;">
            <span class="{light}"></span>
        </div>

        <p class="status-text">
        {result["status"]}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Bridge Status:",
        row["Bridge Running Status"]
    )

    st.write(
        "Blowdown Valve Status:",
        row["Blowdown Valve Status"]
    )

# =====================
# SINGLE VIEW
# =====================

if view_mode == "Single Location":

    selected = st.sidebar.selectbox(
        "Location",
        locations
    )

    draw_unit(selected)

# =====================
# MULTI VIEW
# =====================

else:

    selected = st.sidebar.multiselect(
        "Locations",
        locations,
        default=locations
    )

    cols = st.columns(2)

    for i, loc in enumerate(selected):

        with cols[i % 2]:

            draw_unit(loc)
