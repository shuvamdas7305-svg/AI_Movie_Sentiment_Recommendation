import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os 
from dotenv import load_dotenv

# Page Configuration Initialization
load_dotenv()
st.set_page_config(page_title="CineMatch AI | Taste Analyzer", page_icon="🎬", layout="wide")
BACKEND_URL = "http://127.0.0.1:8000"

for key in ["selected_rec", "rec_data_cache", "analysis_cache"]:
    if key not in st.session_state: st.session_state[key] = None

# =========================================================================
# ADVANCED CYBERPUNK UI ENGINE: CURSOR GLOW, CUSTOM RADAR & APP PRELOADER
# =========================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    /* Global Canvas Styling Reset */
    html, body, [data-testid="stAppViewContainer"] {
        background: #090a0f !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important; color: #f3f4f6 !important;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }

    /* 🏎️ INSTANT GLOBAL APP LOADING SPIN ANIMATION OVERLAY */
    #stAppViewContainer::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: #060709; z-index: 999999; opacity: 1; pointer-events: none;
        animation: fadeOutLoader 0.8s ease forwards 0.4s;
    }
    @keyframes fadeOutLoader { to { opacity: 0; display: none; } }

    /* ✨ INTERACTIVE MOUSE REACTION BACKDROP LAYER */
    .bg-animation {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none;
        background: radial-gradient(circle at var(--mouse-x, 25%) var(--mouse-y, 30%), rgba(255, 75, 75, 0.07) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(30, 40, 70, 0.1) 0%, transparent 60%);
        transition: background 0.1s linear;
    }

    /* Structural Containers */
    .hero-container {
        text-align: center; padding: 2rem; border-radius: 20px;
        background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px); box-shadow: 0 20px 50px rgba(0,0,0,0.4); margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 2.6rem; font-weight: 800; margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF7676 60%, #FFFFFF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .dashboard-panel {
        background: rgba(18, 19, 23, 0.65) !important; backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 24px; margin-bottom: 2rem;
    }

    /* Left Hand Side Cards List Engine */
    .movie-card {
        padding: 18px; border-radius: 12px; margin-bottom: 12px;
        background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.04); border-left: 5px solid rgba(255,255,255,0.1);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.2), border-color 0.3s, background 0.3s;
    }
    .movie-card:hover {
        transform: translateY(-2px) scale(1.015); background: rgba(255, 255, 255, 0.04) !important;
        border-left-color: #FF7676; box-shadow: 0 8px 25px rgba(255, 75, 75, 0.08);
    }
    @keyframes pulse-glow {
        0%, 100% { border-color: rgba(255, 75, 75, 0.4); box-shadow: 0 0 15px rgba(255, 75, 75, 0.15); }
        50% { border-color: rgba(255, 118, 118, 0.8); box-shadow: 0 0 25px rgba(255, 75, 75, 0.3); }
    }
    .card-active {
        transform: scale(1.03) !important; border-left-color: #FF4B4B !important;
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.06) 0%, rgba(14, 15, 19, 0.9) 70%) !important;
        animation: pulse-glow 2.5s infinite ease-in-out;
    }

    /* Right Hand Side Details Inspection Box Styling */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .detail-panel {
        background: rgba(14, 15, 19, 0.85) !important; 
        border: 1px solid rgba(255, 255, 255, 0.06); border-top: 3px solid #FF4B4B;
        border-radius: 14px; padding: 22px; backdrop-filter: blur(25px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .detail-header-card {
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 10px; padding: 14px; margin: 12px 0;
    }
    .pill-tag {
        display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600;
        background: rgba(255, 75, 75, 0.1); color: #FF7676; border: 1px solid rgba(255, 75, 75, 0.2); margin-right: 6px;
    }
    .pill-score {
        display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600;
        background: rgba(255, 255, 255, 0.03); color: #e5e7eb; border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .detail-text-body {
        font-size: 0.95rem; line-height: 1.55; color: #cbd5e1; 
        background: rgba(0, 0, 0, 0.2); border-radius: 8px; padding: 12px; border: 1px solid rgba(255,255,255,0.01);
    }

    /* Core Interaction Form Items */
    .stButton>button {
        background: linear-gradient(135deg, #FF4B4B 0%, #D32F2F 100%) !important; color: white !important;
        border: none !important; border-radius: 8px !important; font-weight: 600 !important;
        transition: all 0.2s ease !important; margin-top: 2px;
    }
    .stButton>button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 12px rgba(255, 75, 75, 0.35) !important; }
</style>

<div class="bg-animation" id="ambient-canvas"></div>

<script>
    // Live Dynamic Mouse Coordinate Interaction Script
    const bg = document.getElementById('ambient-canvas');
    window.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth) * 100;
        const y = (e.clientY / window.innerHeight) * 100;
        bg.style.setProperty('--mouse-x', x + '%');
        bg.style.setProperty('--mouse-y', y + '%');
    });
</script>
""", unsafe_allow_html=True)

# ==========================================
# HELPER DATA PIPELINE INTEGRATIONS
# ==========================================
def map_taste_parameters(genres):
    m = {k: 10 for k in ["Adrenaline & Stakes", "Emotional Depth", "Intellectual / Plot Complexity", "Atmosphere & Escapism", "Character Realism / Grit"]}
    for g in genres:
        if g == "Action": m["Adrenaline & Stakes"]+=50; m["Character Realism / Grit"]+=20
        elif g == "Biography": m["Character Realism / Grit"]+=50; m["Emotional Depth"]+=30
        elif g == "Comedy": m["Atmosphere & Escapism"]+=45; m["Adrenaline & Stakes"]+=10
        elif g == "Crime": m["Intellectual / Plot Complexity"]+=40; m["Character Realism / Grit"]+=45
        elif g == "Drama": m["Emotional Depth"]+=50; m["Character Realism / Grit"]+=30
        elif g == "Horror": m["Atmosphere & Escapism"]+=50; m["Adrenaline & Stakes"]+=30
        elif g == "Sci-Fi": m["Intellectual / Plot Complexity"]+=50; m["Atmosphere & Escapism"]+=35
        elif g == "Animation": m["Atmosphere & Escapism"]+=50; m["Emotional Depth"]+=25
    return {k: min(v, 100) for k, v in m.items()}

def query_gemini(prompt_payload):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "⚠️ Setup Error: `GEMINI_API_KEY` is missing."
    models = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt_payload}]}]}, timeout=10)
            if res.status_code == 200: return res.json()['candidates'][0]['content']['parts'][0]['text']
        except: pass
    return "🚨 Generation Cluster Timeout. Failed to fetch narrative metrics."

# ==========================================
# APPLICATION RENDER LAYER MATRIX
# ==========================================
st.markdown('<div class="hero-container"><h1 class="hero-title">🎬 CineMatch AI: Generative Taste Profiler</h1><p style="color: #94a3b8; margin:0; font-size:0.95rem;">Compile interactive custom narrative metrics and tracking matrices instantly.</p></div>', unsafe_allow_html=True)

genres_pool = ["Action", "Biography", "Comedy", "Crime", "Drama", "Horror", "Sci-Fi", "Animation"]
chosen_genres = st.multiselect("Configure targeted preference frameworks:", options=genres_pool, default=["Action", "Sci-Fi"])

if st.button("⚡ Execute Deep Profile Analysis", type="primary"):
    if not chosen_genres:
        st.warning("⚠️ Select at least one framework variable.")
    else:
        st.session_state.selected_rec = None 
        user_metrics = map_taste_parameters(chosen_genres)
        
        with st.spinner("✨ Mapping Taste Architectures via Gemini Framework Matrix..."):
            p_text = ", ".join([f"{k}: {v}/100" for k, v in user_metrics.items()])
            st.session_state.analysis_cache = query_gemini(
                f"You are a cinema psychologist. Analyze these movie preferences. Genres: {', '.join(chosen_genres)}. Metrics: {p_text}. "
                f"Provide a short, clean bulleted analysis framework summarizing psychological taste drivers under 120 words total."
            )
            
        primary_genre = chosen_genres[0]
        try:
            res = requests.get(f"{BACKEND_URL}/recommend", params={"genre": primary_genre}, timeout=10)
            st.session_state.rec_data_cache = res.json() if res.status_code == 200 else []
        except requests.exceptions.ConnectionError:
            st.session_state.rec_data_cache = "connection_error"

if st.session_state.analysis_cache:
    user_metrics = map_taste_parameters(chosen_genres)
    
    # 1) REMODALED DOCK CONTAINER LINKING RADAR GRAPH INTERACTIVE INTERFACE
    st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
    top_l, top_r = st.columns([52, 48], gap="large")
    with top_l:
        st.markdown("#### 🧠 AI Psychological Profile Summary")
        st.markdown(st.session_state.analysis_cache)
    with top_r:
        st.markdown("<h4 style='margin:0 0 10px 0;'>📊 Parametric Vector Distribution Mapping</h4>", unsafe_allow_html=True)
        df_chart = pd.DataFrame({'Dimension': list(user_metrics.keys()), 'Value': list(user_metrics.values())})
        
        # Highly Custom Designed Cyberpunk Theme Layout Vector Plot Matrix
        fig = px.line_polar(df_chart, r='Value', theta='Dimension', line_close=True, range_r=[0, 100], color_discrete_sequence=['#FF4B4B'])
        fig.update_traces(fill='toself', fillcolor='rgba(255, 75, 75, 0.2)', line=dict(width=3, color='#FF4B4B'))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, showticklabels=False, gridcolor='rgba(255,255,255,0.08)', linecolor='rgba(0,0,0,0)'),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.08)', 
                    color='#94a3b8', 
                    tickfont=dict(size=10, family='Plus Jakarta Sans')  # FIXED: Changed 'font' to 'tickfont'
                ),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", 
            showlegend=False, 
            height=240, 
            margin=dict(l=45, r=45, t=15, b=15)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # 2) LOWER RECOMMENDATIONS COLUMN SPLIT
    st.markdown("### 🎬 Custom-Tailored Cinematic Match Rankings")
    if st.session_state.rec_data_cache == "connection_error":
        st.error("🚨 Connection dropped: Validate if backend cluster `server.py` is operational on Port 8000.")
    elif not st.session_state.rec_data_cache:
        st.info("No matching records found inside current database architecture.")
    else:
        btm_l, btm_r = st.columns([45, 55], gap="large")
        
        with btm_l:
            st.caption("💡 Select a movie card below to populate tracking parameters:")
            for idx, item in enumerate(st.session_state.rec_data_cache[:3], 1):
                rec_id = f"movie_{idx}"
                is_sel = (st.session_state.selected_rec == rec_id)
                card_class = "movie-card card-active" if is_sel else "movie-card"
                
                st.markdown(f"""
                <div class="{card_class}">
                    <h4 style='margin:0 0 4px 0; color:#fff;'>#{idx} {item['movie_title']} <span style='font-size:0.85rem; color:#64748b;'>({item['release_year']})</span></h4>
                    <p style='margin:0; font-size:0.88rem; color:#94a3b8;'>⭐ Rating: <b style='color:#fff;'>{item['rating']}/10</b> | <span>{item['genre']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Inspect Analysis #{idx}", key=f"btn_{rec_id}", use_container_width=True):
                    st.session_state.selected_rec = rec_id
                    st.rerun()

        with btm_r:
            if st.session_state.selected_rec:
                item_idx = int(st.session_state.selected_rec.split("_")[1]) - 1
                active_match = st.session_state.rec_data_cache[item_idx]
                
                # FIXED: Container matches cards list sizing symmetrically with zero trailing space leaks
                st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
                st.markdown(f"<h3 style='margin:0; color:#fff; font-weight:800; font-size:1.3rem;'>📊 Vector Depth Metrics</h3>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="detail-header-card">
                    <h4 style='margin:0 0 8px 0; color:#FF7676; font-size:1.1rem;'>{active_match['movie_title']}</h4>
                    <span class="pill-tag">🎭 Context: {active_match['genre']}</span>
                    <span class="pill-score">⭐ Alignment: {active_match['rating']}/10</span>
                </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("Analyzing narrative vector architectures..."):
                    deep_insights = query_gemini(
                        f"Analyze '{active_match['movie_title']}' ({active_match['description']}) in genre {active_match['genre']}. "
                        f"Provide a brief paragraph breakdown explaining its thematic setup under 100 words max."
                    )
                
                st.markdown(f'<div class="detail-text-body">{deep_insights}</div>', unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)
                
                if st.button("Close Detailed Inspection Panel ✕", use_container_width=True):
                    st.session_state.selected_rec = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Symmetrical fallback viewport filling space perfectly
                st.markdown("<div style='border: 2px dashed rgba(255,255,255,0.04); border-radius:14px; padding:65px 20px; text-align:center; min-height: 240px; display: flex; flex-direction: column; justify-content: center;'><p style='color:#64748b; margin:0;'>👈 Select a cinematic match tracking card on the left to unpack deep feature vectors instantly.</p></div>", unsafe_allow_html=True)