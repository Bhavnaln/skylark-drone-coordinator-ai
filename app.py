import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import json

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Drone Operations Coordinator",
    layout="wide"
)

# --------------------------------------------------
# GOOGLE SHEETS CONNECTION
# --------------------------------------------------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# ✅ CLOUD + LOCAL COMPATIBILITY

try:
    # Use Streamlit Cloud secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, scope)

except:
    # Fallback for local run
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1oGCzIXG-YESjQHBxZ_q7qEOuMR9CC2nAWywNGxD135w/edit?gid=1237425074#gid=1237425074"
)


pilot_sheet = sheet.worksheet("pilot_roster")
drone_sheet = sheet.worksheet("drone_fleet")
mission_sheet = sheet.worksheet("missions")

pilots = pd.DataFrame(pilot_sheet.get_all_records())
drones = pd.DataFrame(drone_sheet.get_all_records())
missions = pd.DataFrame(mission_sheet.get_all_records())

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("Drone Operations System")

section = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Pilot Management", "Drone Inventory",
     "Mission Assignment", "Urgent Reassignment"]
)

# =====================================================
# DASHBOARD
# =====================================================

if section == "Dashboard":

    st.title("Drone Operations Coordinator")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Pilots", len(pilots))
    col2.metric("Total Drones", len(drones))
    col3.metric("Active Missions", len(missions))

# =====================================================
# PILOT MANAGEMENT
# =====================================================

elif section == "Pilot Management":

    st.title("Pilot Management")

    st.subheader("Pilot Roster")
    st.dataframe(pilots)

    st.subheader("Search Available Pilots")

    col1, col2 = st.columns(2)
    skill = col1.text_input("Required Skill")
    location = col2.text_input("Location")

    if st.button("Search Pilots"):

        with st.spinner("Processing request..."):
            time.sleep(1)

            filtered = pilots[pilots["status"] == "Available"]

            if skill:
                filter
