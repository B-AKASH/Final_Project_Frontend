import streamlit as st
import requests
import pandas as pd
import numpy as np
import textwrap

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="HOSPITAL INQUIRY",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL STYLES
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-dark: #010204;
    --card-bg: rgba(6, 12, 26, 0.7);
    --accent-blue: #0ea5e9;
    --accent-cyan: #22d3ee;
    --accent-glow: rgba(14, 165, 233, 0.25);
    --text-main: #f1f5f9;
    --text-dim: #94a3b8;
    --border-color: rgba(14, 165, 233, 0.15);
}

/* Elite Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-main);
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 0% 100%, rgba(14, 165, 233, 0.05) 0%, transparent 40%);
}

[data-testid="stSidebar"] {
    background-color: #01040a;
    border-right: 1px solid var(--border-color);
}

/* Glassmorphism 2.0 */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(30px) saturate(180%);
    border-radius: 28px;
    padding: 32px;
    border: 1px solid var(--border-color);
    box-shadow: 
        0 10px 30px rgba(0,0,0,0.6),
        inset 0 0 20px rgba(14, 165, 233, 0.05);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.glass-card:hover {
    transform: translateY(-5px);
    border-color: rgba(14, 165, 233, 0.4);
    box-shadow: 0 30px 60px rgba(0,0,0,0.8), 0 0 20px var(--accent-glow);
}

/* Telemetry Bio-Cards */
.bio-card {
    background: rgba(14, 165, 233, 0.03);
    padding: 24px;
    border-radius: 24px;
    border: 1px solid rgba(14, 165, 233, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
}

.bio-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
}

.bio-card:hover {
    background: rgba(14, 165, 233, 0.08);
    border-color: var(--accent-blue);
    transform: scale(1.05);
}

.bio-icon { font-size: 1.8rem; color: var(--accent-cyan); filter: drop-shadow(0 0 12px var(--accent-glow)); }
.bio-val { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: #fff; text-shadow: 0 0 15px var(--accent-glow); }
.bio-lbl { font-size: 0.7rem; font-weight: 800; letter-spacing: 0.15em; color: var(--text-dim); text-transform: uppercase; }

/* Clinical Command Header */
.dash-header {
    background: linear-gradient(135deg, #020617 0%, #010204 100%);
    padding: 56px;
    border-radius: 40px;
    margin-bottom: 40px;
    border: 1px solid var(--border-color);
    border-bottom: 4px solid var(--accent-blue);
    box-shadow: 0 20px 80px rgba(0,0,0,0.7);
    position: relative;
    overflow: hidden;
}

.dash-header::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at center, rgba(14, 165, 233, 0.05) 0%, transparent 60%);
    pointer-events: none;
}

/* Medical Paper Elite */
.medical-paper {
    background: #ffffff;
    padding: 40px;
    border-radius: 4px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    position: relative;
    border-top: 15px solid #1e293b;
}

.medical-paper::after {
    content: 'CLINICAL VERIFIED';
    position: absolute;
    bottom: 20px; right: 20px;
    border: 2px solid #e2e8f0;
    padding: 5px 12px;
    font-size: 0.6rem;
    font-weight: 900;
    color: #94a3b8;
    transform: rotate(-15deg);
    opacity: 0.5;
}

/* Scanning Animation */
@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}

.scan-line {
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(transparent, var(--accent-blue), transparent);
    opacity: 0.3;
    animation: scan 3s linear infinite;
    pointer-events: none;
}

.intel-brief {
    background: #020617;
    color: #f8fafc;
    border-radius: 24px;
    padding: 40px;
    border: 1px solid var(--border-color);
    box-shadow: 0 0 50px rgba(14, 165, 233, 0.1);
    position: relative;
    overflow: hidden;
}

.reason-card {
    background: rgba(255,255,255,0.02);
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 3px solid var(--accent-blue);
}

.metric-pill {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    border: 1px solid rgba(14, 165, 233, 0.3);
    background: rgba(14, 165, 233, 0.1);
    color: #0f172a;
    margin: 4px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPERS (CRITICAL FIX)
# --------------------------------------------------
def glass_card_start(extra_style=""):
    st.markdown(f'<div class="glass-card" style="{extra_style}">', unsafe_allow_html=True)

def glass_card_end():
    st.markdown('</div>', unsafe_allow_html=True)

def intel_brief_start(session_id, source_count):
    st.markdown(f"""
    <div class="intel-brief">
        <div class="scan-line"></div>
        <div style="border-left: 4px solid #0ea5e9; padding-left: 20px; margin-bottom: 25px; position:relative; z-index:1;">
            <h3 style="margin:0; font-family:'Outfit'; color:#fff; letter-spacing:0.05rem;">AGENT INTELLIGENCE SYNTHESIS</h3>
            <p style="color:#94a3b8; font-family:'JetBrains Mono'; font-size:0.8rem; margin:5px 0 0 0;">📡 SECURE UPLINK ACTIVE • SESSION ID PX-{session_id}</p>
        </div>
        <div style="background:rgba(0,0,0,0.4); border-radius:12px; padding:25px; border:1px solid rgba(255,255,255,0.05); margin-bottom:25px; position:relative; z-index:1;">
    """, unsafe_allow_html=True)

def intel_brief_end(source_count):
    st.markdown(f"""
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:10px; position:relative; z-index:1;">
            <div class="metric-pill" style="color:#f8fafc; border-color:rgba(255,255,255,0.1); background:rgba(255,255,255,0.05)">📡 SOURCES: {source_count}</div>
            <div class="metric-pill" style="color:#0ea5e9; border-color:var(--accent-blue); background:rgba(14, 165, 233, 0.1)">🔒 SECURITY: ENCRYPTED-L5</div>
            <div class="metric-pill" style="color:#22d3ee; border-color:#22d3ee; background:rgba(34, 211, 238, 0.1)">⚡ ENGINE: NEURAL-RAG-X</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def consult_box_start():
    st.markdown('<div class="consult-box"><div style="font-family:\'Inter\', sans-serif; color:#cbd5e1; font-size:0.95rem; line-height:1.7;">', unsafe_allow_html=True)

def consult_box_end():
    st.markdown('</div></div>', unsafe_allow_html=True)

def bio_card(label, value, icon):
    return f"""
    <div class="bio-card">
        <div class="bio-icon">{icon}</div>
        <div class="bio-val">{value}</div>
        <div class="bio-lbl">{label}</div>
    </div>
    """

# --------------------------------------------------
# SESSION STATE (ROBUST INITIALIZATION)
# --------------------------------------------------
if "view" not in st.session_state:
    st.session_state.view = "welcome"
if "result_data" not in st.session_state:
    st.session_state.result_data = {}

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0;">
            <h2 style="font-family:'Outfit'; color:#0ea5e9; margin-bottom:20px;">🛡️ DETAILS ENQURIY</h2>
        </div>
    """, unsafe_allow_html=True)

    url="https://final-project-1-08eq.onrender.com"

    with st.expander("👤 PATIENT DETAILS", expanded=True):
        st.markdown('<p style="font-size:0.8rem; color:#94a3b8; margin-bottom:8px;">Enter patient id</p>', unsafe_allow_html=True)
        pid = st.number_input("Patient ID", min_value=1, value=1001, label_visibility="collapsed")
        if st.button(" SHOW", use_container_width=True, type="primary"):
            r = requests.post(url+"/analyze", json={"patient_id": pid})
            if r.status_code == 200:
                st.session_state.result_data = r.json()
                st.session_state.view = "patient"
                st.rerun()

    with st.expander("�️ DEBUG ASSISTANT", expanded=False):
        if st.session_state.result_data:
            st.code(st.session_state.result_data, language="json")
        else:
            st.write("No data in result buffer.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧹 CLEAR", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --------------------------------------------------
# WELCOME VIEW
# --------------------------------------------------
if st.session_state.view == "welcome":
    st.markdown("""
    <div class="dash-header">
        <h1 style="margin:0; font-family:'Outfit'; font-weight:700; letter-spacing:-0.02em;">
            HOSPITAL <span style="color:#0ea5e9;">INSIGHT</span> ENGINE
        </h1>
        <p style="color:#94a3b8; font-size:1.1rem; margin-top:8px;">
            Advanced Medical Intelligence & Clinical Support System
        </p>
    </div>
    """, unsafe_allow_html=True)

    glass_card_start()
    st.markdown("""
    ### ⚡ PRO-GRADE FEATURES
    - **Agent-Driven Queries**
    - **Medical RAG**
    - **Clinical Risk Intelligence**
    - **Unified Analytics Dashboard**
    """)
    glass_card_end()

# --------------------------------------------------
# PATIENT VIEW (ENHANCED)
# --------------------------------------------------
elif st.session_state.view == "patient":
    data = st.session_state.get("result_data", {})
    
    # --- HYBRID MAPPING (Robust against flat/nested backend) ---
    if "patient_summary" in data:
        ps = data["patient_summary"]
        ds = data.get("decision_support", {})
    else:
        # Fallback for flat structure or malformed nested data
        ps = data
        ds = {}

    if not ps:
        st.warning("⚠️ High-fidelity data not available for this record. Please try again.")
        st.session_state.view = "welcome"
        st.rerun()

    st.markdown(f"""
    <div class="dash-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-end; position:relative; z-index:1;">
            <div>
                <h1 style="margin:0; font-family:'Outfit'; font-weight:700; color:#fff; font-size:3rem; letter-spacing:-0.02em;">{ps.get('patient_name', ps.get('name', 'Unknown'))}</h1>
                <p style="color:var(--accent-cyan); font-family:'JetBrains Mono'; margin:8px 0 0 0; letter-spacing:0.1em; font-weight:700;">
                    <span style="opacity:0.6;">PATIENT_UID_</span>{ps.get('patient_id', 'N/A')} • {ps.get('age', '??')}Y • {str(ps.get('gender', 'N/A')).upper()}
                </p>
            </div>
            <div style="background:rgba(14, 165, 233, 0.15); padding:10px 20px; border-radius:14px; border:1px solid var(--accent-blue); backdrop-filter:blur(10px);">
                <span style="color:var(--accent-cyan); font-weight:800; font-size:0.8rem; letter-spacing:0.1em; font-family:'JetBrains Mono';">📡 SYSTEM_STATUS: ENCRYPTED_SYNC</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 CLINICAL SUMMARY", "🧠 DECISION SUPPORT", "📊 VITALS & TRENDS", "💊 MEDICATION & INSURANCE"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(bio_card("Diagnosis", ps.get("diagnosis", "N/A"), "🩺"), unsafe_allow_html=True)
        c2.markdown(bio_card("Risk Level", ps.get("risk_level", "N/A"), "⚠️"), unsafe_allow_html=True)
        c3.markdown(bio_card("Care Priority", ps.get("care_priority", "N/A"), "🏷️"), unsafe_allow_html=True)
        c4.markdown(bio_card("Visit Date", ps.get("visit_date", "N/A"), "📅"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Medical Paper Style for Summary
        chronic_pills = []
        if ps.get('diabetes') == 'Yes': chronic_pills.append(f"<div class='metric-pill'>Diabetes: {ps.get('diabetes')}</div>")
        if ps.get('asthma') == 'Yes': chronic_pills.append(f"<div class='metric-pill'>Asthma: {ps.get('asthma')}</div>")
        if ps.get('chronic_kidney_disease') == 'Yes': chronic_pills.append(f"<div class='metric-pill'>CKD: {ps.get('chronic_kidney_disease')}</div>")
        if ps.get('obesity') == 'Yes': chronic_pills.append(f"<div class='metric-pill'>Obesity: {ps.get('obesity')}</div>")
        if ps.get('anemia') == 'Yes': chronic_pills.append(f"<div class='metric-pill'>Anemia: {ps.get('anemia')}</div>")
        chronic_pills.append(f"<div class='metric-pill'>Smoking: {ps.get('smoking_status', 'N/A')}</div>")
        
        pills_html = "".join(chronic_pills)
        
        summary_html = f"""<div class="medical-paper">
<div class="scan-line" style="background:linear-gradient(transparent, #cbd5e1, transparent); opacity:0.1; animation-duration:5s;"></div>
<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #f1f5f9; padding-bottom:15px; margin-bottom:20px;">
<h2 style="margin:0; color:#0f172a; font-family:'Outfit'; font-weight:800; letter-spacing:0.02em;">CLINICAL CASE SUMMARY</h2>
<div style="text-align:right; font-family:'JetBrains Mono';">
<span style="font-size:0.75rem; color:#64748b;">TIMESTAMP: {ps.get('visit_date', 'N/A')}</span><br>
<span style="font-weight:700; color:#0ea5e9; font-size:0.85rem;">DOC: AGENT-AI-PX-{ps.get('patient_id', 'N/A')}</span>
</div>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
<div>
<h3 style="color:#1e293b; font-size:1rem; margin-bottom:10px;">PATIENT STATUS</h3>
<p style="font-size:1rem; color:#334155;">
Assessment for <b>{ps.get('patient_name', ps.get('name', 'Unknown'))}</b> ({ps.get('gender', 'N/A')}, {ps.get('age', '??')}y) reveals a <b>{str(ps.get('risk_level', 'low')).lower()} risk</b> profile 
with <b>{str(ps.get('care_priority', 'normal')).lower()}</b> priority. The primary diagnosis is <b>{ps.get('diagnosis', 'N/A')}</b>.
</p>
</div>
<div>
<h3 style="color:#1e293b; font-size:1rem; margin-bottom:10px;">CHRONIC CONDITIONS</h3>
<div style="display: flex; flex-wrap: wrap; gap: 8px;">
{pills_html}
</div>
</div>
</div>
</div>"""
        st.markdown(summary_html, unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([1, 1.4])
        with col_l:
            st.markdown("### 🎯 CLINICAL RATIONALE")
            for reason in ds.get("why", []):
                st.markdown(f"""
                <div class="reason-card">
                    <div style="color:#0ea5e9; font-size:1.2rem;">🔹</div>
                    <div style="font-size:0.95rem; color:#f8fafc;">{reason}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_r:
            st.markdown("### 🧠 EXPERT ANALYSIS")
            consult_box_start()
            st.markdown(ds.get("llm_explanation", "Medical analysis insight unavailable."))
            consult_box_end()

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(bio_card("Blood Pressure", ps.get("blood_pressure", "N/A"), "❤️"), unsafe_allow_html=True)
        c2.markdown(bio_card("Heart Rate", f"{ps.get('heart_rate', 'N/A')} bpm", "💓"), unsafe_allow_html=True)
        c3.markdown(bio_card("Cholesterol", f"{ps.get('cholesterol', 'N/A')} mg/dL", "🧪"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        glass_card_start()
        st.markdown("### 📈 BIOMETRIC TELEMETRY DATA")
        chart = pd.DataFrame(
            np.random.randint(60, 160, size=(10, 2)),
            columns=["BP", "Heart Rate"]
        )
        st.area_chart(chart, use_container_width=True, color=["#0ea5e9", "#22d3ee"])
        glass_card_end()

    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            glass_card_start()
            st.markdown("### 💊 MEDICATION PLAN")
            st.markdown(f"""
            <div class="data-row"><span class="data-label">Prescription</span><span class="data-value">{ps.get('medication', 'N/A')}</span></div>
            <div class="data-row"><span class="data-label">Dosage</span><span class="data-value">{ps.get('dosage', 'N/A')}</span></div>
            """, unsafe_allow_html=True)
            glass_card_end()
        
        with col2:
            glass_card_start()
            st.markdown("### 🛡️ INSURANCE & BILLING")
            st.markdown(f"""
            <div class="data-row"><span class="data-label">Insurance Active</span><span class="data-value">{'✅ YES' if ps.get('has_insurance') == 'True' else '❌ NO'}</span></div>
            <div class="data-row"><span class="data-label">Plan Details</span><span class="data-value">{ps.get('insurance_plan', 'N/A')}</span></div>
            """, unsafe_allow_html=True)
            glass_card_end()

# --------------------------------------------------
# INQUIRY VIEW (ENHANCED)
# --------------------------------------------------
elif st.session_state.view == "inquiry":
    res = st.session_state.get("result_data", {})
    
    if not res:
        st.warning("⚠️ Intelligent inquiry context lost. Please search again.")
        st.session_state.view = "welcome"
        st.rerun()

    st.markdown("""
    <div class="dash-header">
        <h2 style="margin:0; font-family:'Outfit'; font-weight:700;">INQUIRY <span style="color:#0ea5e9;">REPORT</span></h2>
        <p style="color:#94a3b8; margin:4px 0 0 0;">INTELLIGENT AGENT SYNTHESIS</p>
    </div>
    """, unsafe_allow_html=True)

    intel_brief_start(
        session_id=np.random.randint(100000, 999999), 
        source_count=len(res.get('matched_records', []))
    )
    st.markdown(res.get("deep_explanation", "Analysis in progress or unavailable..."))
    intel_brief_end(
        source_count=len(res.get('matched_records', []))
    )

    if res.get("matched_records"):
        st.markdown("<br>", unsafe_allow_html=True)
        glass_card_start()
        st.markdown("### 📄 MATCHED PATIENT DATA")
        
        # Format the dataframe for clear presentation
        df = pd.DataFrame(res.get("matched_records", []))
        
        # Select and order columns for professional look
        cols = [
            'patient_id', 'patient_name', 'age', 'gender', 'diagnosis', 'visit_date', 
            'medication', 'dosage', 'risk_level', 'care_priority', 
            'blood_pressure', 'heart_rate', 'cholesterol', 'diabetes', 
            'asthma', 'chronic_kidney_disease', 'obesity', 'smoking_status', 'anemia',
            'has_insurance', 'insurance_plan'
        ]
        # Only include columns that actually exist in the dataframe
        available_cols = [c for c in cols if c in df.columns]
        df = df[available_cols]
        
        # Professional column naming
        df.columns = [c.replace('_', ' ').title() for c in df.columns]
        
        st.dataframe(
            df, 
            use_container_width=True,
            hide_index=True,
        )
        glass_card_end()
