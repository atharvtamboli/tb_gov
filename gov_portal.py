import streamlit as st
import pandas as pd
from supabase import create_client, Client
import time

# --- 1. CONFIGURATION ---
# REPLACE WITH YOUR REAL KEYS
SUPABASE_URL = "https://vsvdddwigtestjoaksry.supabase.co"
SUPABASE_KEY = "sb_publishable_Z-NPHhciBw1XDK4SxAPUow_A9U_vmsw"

# Connect to DB
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("System Error: Database connection failed. Check API Keys.")

# --- 2. PAGE SETUP ---
st.set_page_config(
    page_title="Raj-Ni-Kshay | Govt of Rajasthan", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. PROFESSIONAL GOVERNMENT CSS (FINAL VISIBILITY FIX) ---
st.markdown("""
    <style>
    /* 1. Force Global Light Theme */
    .stApp {
        background-color: #f8f9fa !important;
    }
    
    /* 2. FORCE SIDEBAR WHITE & BLACK TEXT */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #dcdcdc;
    }
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* 3. FORCE INPUTS (Dropdowns, Time, Text) TO BE WHITE */
    /* This fixes the invisible "Select Patient" box */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Force text inside dropdowns to be black */
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    
    /* Fix the popup menu in dropdowns */
    ul[role="listbox"] {
        background-color: #ffffff !important;
    }
    li[role="option"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* 4. General Text Color (Black) */
    p, h1, h2, h3, h4, h5, label, div, span, li { 
        color: #212529 !important; 
    }

    /* 5. Header Design */
    .gov-header {
        background-color: #0034a5;
        padding: 1.5rem;
        border-bottom: 5px solid #ff9933;
        color: white !important;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
    .gov-header h2, .gov-header p { color: white !important; }

    /* 6. Login Box Styling */
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 5px solid #0034a5;
    }
    
    /* 7. Google Button Visual */
    .google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background: white;
        color: #333 !important;
        font-weight: 500;
        cursor: pointer;
        margin-bottom: 15px;
        transition: 0.2s;
    }
    .google-btn:hover { background-color: #f1f1f1; }
    
    /* 8. Components */
    div[data-testid="stMetric"], div[data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border: 1px solid #dee2e6;
        padding: 15px;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #0034a5;
        color: white !important;
        width: 100%;
    }
    
    /* Fix Tabs */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0034a5 !important;
        border-bottom: 2px solid #0034a5 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTHENTICATION LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Login Container Start
        st.markdown("""
            <div class="login-container">
                <div style="text-align: center;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" width="50">
                    <h3 style="margin-top: 10px;">Raj-Ni-Kshay Portal</h3>
                    <p style="font-size: 12px; color: #666;">Medical & Health Department</p>
                </div>
        """, unsafe_allow_html=True)

        # Login/Signup Tabs
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])

        with tab1:
            st.markdown("##### Officer Login")
            
            st.markdown("""
                <button class="google-btn">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" width="18" style="margin-right: 10px;">
                    Sign in with Google
                </button>
            """, unsafe_allow_html=True)
                
            st.markdown("<div style='text-align: center; color: #aaa; margin: 10px 0;'>— OR —</div>", unsafe_allow_html=True)

            login_email = st.text_input("Email Address", key="l_email")
            login_pwd = st.text_input("Password", type="password", key="l_pwd")
            
            if st.button("SIGN IN"):
                try:
                    response = supabase.table("officers").select("*").eq("email", login_email).eq("password", login_pwd).execute()
                    if response.data:
                        st.session_state['logged_in'] = True
                        st.session_state['user_name'] = response.data[0]['full_name']
                        st.success("Access Granted.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid Email or Password.")
                except Exception as e:
                    st.error(f"Login Error: {e}")

        with tab2:
            st.markdown("##### New Officer Registration")
            new_name = st.text_input("Full Name (Official)")
            new_email = st.text_input("Official Email")
            new_pwd = st.text_input("Create Password", type="password")
            confirm_pwd = st.text_input("Confirm Password", type="password")

            if st.button("REGISTER ACCOUNT"):
                if new_pwd == confirm_pwd and new_email:
                    try:
                        data = {"full_name": new_name, "email": new_email, "password": new_pwd}
                        supabase.table("officers").insert(data).execute()
                        st.success("Account created! Please Sign In.")
                    except Exception as e:
                        st.error("Error: Email already exists or connection failed.")
                else:
                    st.warning("Passwords do not match or fields empty.")
        
        st.markdown("</div>", unsafe_allow_html=True) 

else:
    # --- 5. MAIN DASHBOARD ---
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/1/1e/Seal_of_Rajasthan.svg", width=100)
        st.markdown(f"**Welcome, {st.session_state['user_name']}**")
        st.caption("District Program Officer")
        st.markdown("---")
        
        page = st.radio("Navigation", ["Dashboard", "Patient Registry", "Manage Records"])
        
        st.markdown("---")
        if st.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.session_state['user_name'] = ""
            st.rerun()

    # HEADER
    st.markdown("""
        <div class="gov-header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" width="70">
            <div style="margin-left: 20px;">
                <h2 style="margin:0; font-size: 26px;">Raj-Ni-Kshay Portal</h2>
                <p style="margin:0; font-size: 14px; opacity: 0.9;">Adherence Monitoring System | Govt of Rajasthan</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- VIEW 1: DASHBOARD ---
    if page == "Dashboard":
        st.subheader("Region Overview: Wagwar")
        response = supabase.table("patients").select("*").execute()
        df = pd.DataFrame(response.data)

        if not df.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Registered Patients", len(df))
            critical = len(df[df['missed_doses'] >= 2])
            m2.metric("Critical Alerts", critical)
            m3.metric("Adherence Rate", "94%")
            m4.metric("Active Calls Today", len(df) * 2)

            st.markdown("---")
            st.subheader("Live Patient Status")
            
            def highlight_critical(row):
                if row['missed_doses'] >= 2:
                    return ['background-color: #ffebee; color: #b71c1c; font-weight: bold'] * len(row)
                return [''] * len(row)

            cols = ['full_name', 'phone_number', 'district', 'missed_doses', 'alarm_time']
            if 'alarm_time_2' in df.columns: cols.append('alarm_time_2')

            st.dataframe(df[cols].style.apply(highlight_critical, axis=1), use_container_width=True)
        else:
            st.info("No records found.")

    # --- VIEW 2: REGISTRY ---
    elif page == "Patient Registry":
        st.subheader("New Beneficiary Registration")
        with st.container():
            st.markdown("<div style='background: white; padding: 20px; border-radius: 5px; border: 1px solid #ddd;'>", unsafe_allow_html=True)
            with st.form("reg_form"):
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("Full Name")
                    phone = st.text_input("Mobile Number (+91...)")
                    aadhaar = st.text_input("Aadhaar ID")
                with c2:
                    district = st.selectbox("District", ["Banswara", "Dungarpur", "Udaipur"])
                    alarm1 = st.time_input("Call Time 1", value=None)
                    alarm2 = st.time_input("Call Time 2", value=None)
                
                if st.form_submit_button("SUBMIT RECORD"):
                    data = {
                        "full_name": name, "phone_number": phone, "aadhaar_number": aadhaar,
                        "district": district, "alarm_time": str(alarm1)[:5] if alarm1 else None,
                        "alarm_time_2": str(alarm2)[:5] if alarm2 else None
                    }
                    supabase.table("patients").insert(data).execute()
                    st.success("Beneficiary added.")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- VIEW 3: MANAGE RECORDS ---
    elif page == "Manage Records":
        st.subheader("Record Management")
        response = supabase.table("patients").select("*").execute()
        df = pd.DataFrame(response.data)

        if not df.empty:
            patient_list = [f"{row['id']} - {row['full_name']}" for index, row in df.iterrows()]
            
            tab1, tab2 = st.tabs(["🕒 Update Time", "🗑️ Delete"])
            
            with tab1:
                st.markdown("#### Change Scheduled Alarm Time")
                sel = st.selectbox("Select Patient", patient_list)
                
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    t1 = st.time_input("New Morning Time", value=None)
                with col_u2:
                    t2 = st.time_input("New Evening Time", value=None)
                
                if st.button("UPDATE TIMINGS"):
                    pid = sel.split(" - ")[0]
                    upd = {}
                    if t1: upd['alarm_time'] = str(t1)[:5]
                    if t2: upd['alarm_time_2'] = str(t2)[:5]
                    supabase.table("patients").update(upd).eq("id", pid).execute()
                    st.success("Updated!")
                    time.sleep(1)
                    st.rerun()

            with tab2:
                st.markdown("#### Remove Beneficiary Permanently")
                sel_d = st.selectbox("Select to Delete", patient_list, key="d")
                if st.button("DELETE RECORD", type="primary"):
                    pid = sel_d.split(" - ")[0]
                    supabase.table("patients").delete().eq("id", pid).execute()
                    st.success("Deleted.")
                    time.sleep(1)
                    st.rerun()