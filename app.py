import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# ১. পেজ কনফিগারেশন ও রেসপন্সিভ স্টাইলিং (Mobile Friendly)
# ==========================================
st.set_page_config(
    page_title="SB Political Consulting",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# অ্যান্টিক ফিল ও মোবাইল ফ্রেন্ডলি CSS স্টাইলিং
st.markdown("""
    <style>
    /* ব্যাকগ্রাউন্ড ও টেক্সট কালার */
    .stApp {
        background-color: #FAF6EE;
        color: #1A2B4C;
    }
    
    /* হেডারের জন্য কাস্টম স্টাইল */
    .header-container {
        background: linear-gradient(135deg, #0D233A 0%, #1A365D 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 4px solid #D97706;
    }
    
    /* বাটন স্টাইলিং (মোবাইলে বড় টাচ টার্গেট) */
    .stButton>button {
        background-color: #0D233A;
        color: #FFFFFF;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 20px;
        width: 100%;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #D97706;
        color: white;
    }
    
    /* ইনপুট বক্স ও ইনপুট কার্ড */
    .css-1r6594q, .stSelectbox, .stTextInput {
        border-radius: 8px;
    }
    
    /* হাইড পাসওয়ার্ড ও এজেন্ট ভিউ কার্ড */
    .agent-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ২. ডেটাবেস/সেশন স্টেট ইনিশিয়ালাইজেশন
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = ""

# স্যাম্পল কোশ্চেন ব্যাংক
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {
            "id": 1,
            "bn": "১. আগামী নির্বাচনে আপনি এলাকা ভিত্তিক প্রধান সমস্যা কোনটি মনে করেন?",
            "hi": "1. आगामी चुनाव में आपके क्षेत्र का मुख्य मुद्दा क्या है?",
            "en": "1. What do you think is the main local issue in the upcoming election?",
            "options": ["রাস্তাঘাট / উন্নয়ন (Roads/Development)", "কর্মসংস্থান (Employment)", "দুর্নীতি (Corruption)", "অন্যান্য (Others)"]
        },
        {
            "id": 2,
            "bn": "২. বর্তমান রাজ্য সরকারের কাজে আপনি কতটা সন্তুষ্ট?",
            "hi": "2. वर्तमान राज्य सरकार के कार्य से आप कितने संतुष्ट हैं?",
            "en": "2. How satisfied are you with the current state government?",
            "options": ["খুবই সন্তুষ্ট (Very Satisfied)", "মোটামুটি (Neutral)", "অসন্তুষ্ট (Dissatisfied)"]
        }
    ]

# স্যাম্পল এজেন্ট লিস্ট
if 'agents' not in st.session_state:
    st.session_state.agents = [
        {"id": "agent01", "name": "Rahul Das", "pass": "1234"},
        {"id": "agent02", "name": "Amit Sharma", "pass": "5678"}
    ]

# ==========================================
# ৩. হেডার ডিজাইন
# ==========================================
st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size: 28px; font-weight: 800; letter-spacing: 1px;">SB POLITICAL CONSULTING</h1>
        <p style="margin:5px 0 0 0; color: #FBBF24; font-size: 14px;">ELECTION SURVEY & STRATEGY DASHBOARD</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# ৪. লগইন পেজ (Admin & Agent)
# ==========================================
if not st.session_state.logged_in:
    st.subheader("🔑 Login Portal")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        input_user = st.text_input("Username / Agent ID")
        input_pass = st.text_input("Password", type="password") # পাসওয়ার্ড হাইড থাকবে
        
        if st.button("LOGIN"):
            # এডমিন লগইন চেক
            if input_user == "skbabul" and input_pass == "Babul123":
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.username = "skbabul"
                st.rerun()
            else:
                # এজেন্ট লগইন চেক
                found_agent = False
                for ag in st.session_state.agents:
                    if ag["id"] == input_user and ag["pass"] == input_pass:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "agent"
                        st.session_state.username = ag["name"]
                        found_agent = True
                        st.rerun()
                
                if not found_agent:
                    st.error("ভুল ইউজারনেম বা পাসওয়ার্ড দিয়েছেন!")

# ==========================================
# ৫. এজেন্ট ভিউ (শুধু মোবাইল সার্ভে ফর্ম)
# ==========================================
elif st.session_state.logged_in and st.session_state.user_role == "agent":
    
    # টপ বার
    c1, c2 = st.columns([3, 1])
    with c1:
        st.write(f"👤 Agent: **{st.session_state.username}**")
    with c2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.divider()
    
    # ভাষা নির্বাচন
    lang = st.radio("🌐 Select Survey Language / ভাষা নির্বাচন করুন:", ["Bengali (বাংলা)", "Hindi (हिंदी)", "English"], horizontal=True)
    
    lang_key = "bn"
    if "Hindi" in lang:
        lang_key = "hi"
    elif "English" in lang:
        lang_key = "en"
        
    st.write("---")
    st.subheader("📋 Field Survey Questions")
    
    # ফর্ম
    with st.form("survey_form"):
        responses = {}
        for idx, q in enumerate(st.session_state.questions):
            st.write(f"**{q[lang_key]}**")
            responses[q["id"]] = st.radio(f"Select option for Q{idx+1}", q["options"], key=f"q_{q['id']}", label_visibility="collapsed")
            st.write("")
        
        st.write("---")
        st.write("🎙️ **Audio Recording & Location:**")
        
        # অডিও ইনপুট (মোবাইলে মাইক্রোফোন খুলবে)
        audio_val = st.audio_input("Record Audio Response (Optional)")
        
        # জিপিএস লোকেশন সিমুলেশন বা ম্যানুয়াল ইনপুট
        loc_confirm = st.checkbox("📍 Attach GPS Location Details", value=True)
        
        submitted = st.form_submit_button("SUBMIT SURVEY")
        if submitted:
            st.success("✅ Survey submitted successfully! Data sent to admin.")

# ==========================================
# ৬. এডমিন ভিউ (FULL DASHBOARD)
# ==========================================
elif st.session_state.logged_in and st.session_state.user_role == "admin":
    
    # সাইডবার কন্ট্রোল
    st.sidebar.title("ADMIN PANEL")
    st.sidebar.write(f"Logged as: **{st.session_state.username}**")
    
    menu = st.sidebar.radio("Navigation", [
        "📊 Dashboard Overview", 
        "❓ Question Management", 
        "👥 Agent Management",
        "🎙️ Field Reports & Audios"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ১. ড্যাশবোর্ড ওভারভিউ ---
    if menu == "📊 Dashboard Overview":
        st.header("Overview & Real-time Analytics")
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Surveys", "1,248", "+12%")
        kpi2.metric("Active Agents", len(st.session_state.agents), "Live")
        kpi3.metric("Total Questions", len(st.session_state.questions), "Active")
        
        st.subheader("Live Survey Response Flow Across India")
        df_dummy = pd.DataFrame({
            "lat": [22.5726, 28.6139, 19.0760, 13.0827],
            "lon": [88.3639, 77.2090, 72.8777, 80.2707]
        })
        st.map(df_dummy)

    # --- ২. কোশ্চেন ম্যানেজমেন্ট ---
    elif menu == "❓ Question Management":
        st.header("Question Bank (Unlimited)")
        
        # নতুন প্রশ্ন যোগ
        with st.expander("➕ Add New Survey Question", expanded=False):
            q_bn = st.text_input("Question in Bengali (বাংলা)")
            q_hi = st.text_input("Question in Hindi (हिंदी)")
            q_en = st.text_input("Question in English")
            opts = st.text_area("Options (Comma Separated)", "Option 1, Option 2, Option 3")
            
            if st.button("Save Question"):
                if q_bn and q_en:
                    new_q = {
                        "id": len(st.session_state.questions) + 1,
                        "bn": f"{len(st.session_state.questions)+1}. {q_bn}",
                        "hi": f"{len(st.session_state.questions)+1}. {q_hi}",
                        "en": f"{len(st.session_state.questions)+1}. {q_en}",
                        "options": [o.strip() for o in opts.split(",")]
                    }
                    st.session_state.questions.append(new_q)
                    st.success("Question Added Successfully!")
                    st.rerun()

        # বিদ্যমান প্রশ্নের তালিকা
        st.subheader("Existing Questions List")
        for i, q in enumerate(st.session_state.questions):
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.write(f"**{q['bn']}**")
                st.caption(f"EN: {q['en']} | HI: {q['hi']}")
            with col_b:
                if st.button("Delete", key=f"del_q_{i}"):
                    st.session_state.questions.pop(i)
                    st.rerun()

    # --- ৩. এজেন্ট ম্যানেজমেন্ট ---
    elif menu == "👥 Agent Management":
        st.header("Field Agent Accounts")
        
        # নতুন এজেন্ট যোগ
        with st.form("add_agent_form"):
            st.subheader("Create New Agent")
            ag_id = st.text_input("Agent ID (e.g. agent03)")
            ag_name = st.text_input("Agent Name")
            ag_pass = st.text_input("Password", type="password") # সিকিউর হাইড পাসওয়ার্ড
            
            if st.form_submit_button("Create Agent Account"):
                if ag_id and ag_pass:
                    st.session_state.agents.append({"id": ag_id, "name": ag_name, "pass": ag_pass})
                    st.success("Agent Account Created!")
                    st.rerun()
                    
        st.subheader("Active Agents")
        for i, ag in enumerate(st.session_state.agents):
            ca, cb, cc = st.columns([2, 2, 1])
            ca.write(f"**ID:** {ag['id']}")
            cb.write(f"**Name:** {ag['name']}")
            if cc.button("Remove", key=f"del_ag_{i}"):
                st.session_state.agents.pop(i)
                st.rerun()

    # --- ৪. রিপোর্ট ও অডিও ---
    elif menu == "🎙️ Field Reports & Audios":
        st.header("Recorded Audio & Location Logs")
        st.info("Here admin can review audio recordings uploaded by agents along with GPS location timestamps.")
        
        # টেবিল ফরম্যাট
        st.write("Recent Submissions:")
        sample_data = pd.DataFrame([
            {"Agent": "Rahul Das", "Time": "10:15 AM", "Location": "Balagarh, Hooghly", "Audio": "Recorded (0:15s)"},
            {"Agent": "Amit Sharma", "Time": "11:02 AM", "Location": "Dadar, Mumbai", "Audio": "Recorded (0:22s)"}
        ])
        st.dataframe(sample_data, use_container_width=True)

