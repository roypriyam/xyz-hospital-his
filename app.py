import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="XYZ Hospital HIS - Phase 1 Prototype", layout="wide")

st.title("XYZ Hospital HIS - Phase 1 Interactive Solution Prototype")
st.caption("Client: XYZ Hospital Limited | Prepared by: Priyam Roy | Version: 1.0")

if "patients_db" not in st.session_state:
    st.session_state.patients_db = {
        "XYZ-2026-1001": {"name": "Rahim Uddin", 'age': 45, 'gender': 'Male', 'phone': '01711000000', 'nid': '1979269123456'},�
        'XYZ-2026-1002': {"name": 'Fatema Begum', 'age': 32, 'gender': 'Female', 'phone': 'O1819111111', 'nid': '1992269654321'},
    }

if "queue_db" not in st.session_state:
    st.session_state.queue_db = [
        {"token": "A-12", "uhid": "XYZ 2026-1001", "name": "Rahim Uddin", "chamber": "Chamber 101 - Cardiology", "status": "In-Consultation"},
        {"token": "A-13", "uhid": "XYZ 2026-1002", "name": "Fatema Begum", "chamber": "Chamber 101 - Cardiology", "status": "Waiting"},
    ]

if "prescriptions_db" not in st.session_state:
    st.session_state.prescriptions_db = []

menu = st.sidebar.radio("Select Module Dashboard:", [
    "Module 1 & 2: Registration & Billing",
    "Module 3: Chamber Queue & TV Display",
    "Module 4: Doctor E-Prescription Workspace",
    "Module 5: Internal Pharmacy POS Sync",
    "How to Deploy to Streamlit Cloud"
])

if "Module 1 & 2" in menu:
    st.header("Module 1 & 2: Patient Registration & Appointment Billing")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Patient Registration")
        nid = st.text_input("NID / Passport Number", value="1995269887766")
        name = st.text_input("Full Name", value="Tanvir Hossain")
        phone = st.text_input("Phone Number", value="01712345678")
    with col2:
        st.subheader("2. Appointment & Billing")
        chamber = st.selectbox("Select Chamber", ["Chamber 101 - Cardiology (Dr. A. K. Azad)", "Chamber 102 - Neurology (Dr. Sharmin Akter)"])
        visit_type = st.selectbox("Visit Category", ["New Consultation (BDT 1,000)", "Follow-up Visit (BDT 500)", "Report Review (FREE)"])
        if st.button("Complete Billing & Issue Entry Pass", type="primary"):
            uhid = f"XYZ-2026-{random.randint(2000,9999)}"
            token = f"A-{len(st.session_state.queue_db)+11}"
            st.session_state.patients_db[uhid] = {"name": name, "phone": phone, "nid": nid}
            st.session_state.queue_db.append({"token": token, "uhid": uhid, "name": name, "chamber": chamber, "status": "Waiting"})
            st.success(f"Registration Successful! Assigned UHID: {uhid} | Token: {token}")

elif "Module 3" in menu:
    st.header("Module 3: Chamber Queue & Lounge TV Display")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Chamber Attendant Console")
        st.dataframe(pd.DataFrame(st.session_state.queue_db))
        if st.button("Call Next Patient", type="primary"):
            st.success("Now Calling Next Serial Token!")
        if st.button("Emergency Override"):
            st.error("Emergency Case Placed at Top of Queue!")
    with col2:
        st.subheader("Lounge TV Display Simulator")
        st.info("NOW CONSULTING: SERIAL A-12 | CHAMBER 101 - CARDIOLOGY")
        st.write("𝔑 Audio Prompt: 'Serial A-12 please enter Chamber 101. সিরিড় -12 চেম�ৈরঀ ী101 এূীূস করੁন.'")

elif "Module 4" in menu:
    st.header("Module 4: Doctor E-Prescription Workspace")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Patient Vitals")
        st.text_input("Blood Pressure", value="120/84")
        st.text_input("Pulse Rate", value="75")
    with col2:
        st.subheader("DGDA Prescription Engine")
        drug = st.selectbox("DGDA Drug Search", ["Napa Extend 665mg (Beximco)", "Seclo 20mg (Square)", "Bisocor 5mg (Incepta)"])
        shorthand = st.text_input("Shorthand Dosage (e.g., 1+0+1 x 7d pc)", value="1+0+1 x 7d pc")
        st.info("Parsed Instruction: 1 tablet Morning, 1 tablet Night for 7 Days (After Food / খঁংংূঀএীঀৃ)")
        if st.button("Finalize & Transmit to Pharmacy POS", type="primary"):
            st.session_state.prescriptions_db.append({"drug": drug, "dosage": shorthand})
            st.success("Prescription Finalized & Auto-Synced to Pharmacy POS via API!")

elif "Module 5" in menu:
    st.header("Module 5: Internal Pharmacy POS Auto-Refill")
    st.subheader("Incoming API Prescription Payload")
    if st.session_state.prescriptions_db:
        st.dataframe(pd.DataFrame(st.session_state.prescriptions_db))
        if st.button("Dispense Medicine & Deduct Inventory", type="primary"):
            st.success("Dispensed! Stock updated instantly without manual data re-typing.")
    else:
        st.info("Waiting for incoming API payload from doctor chamber...")

else:
    st.header("How to Deploy to Streamlit Cloud for Free Shareable Link")
    st.write("""
    1. Upload app.py and requirements.txt to a free public GitHub repository.
    2. Go to share.streamlit.io and click 'New App'.
    3. Select your GitHub repo and click 'Deploy'.
    4. Copy the generated link (e.g. https://xyz-hospital-his.streamlit.app) and paste it into your email submission!
    """)
