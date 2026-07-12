import sys
import subprocess

# Automated User-Space Dependency Resolver for Streamlit Cloud
try:
    import plotly.express as px
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "plotly"])
    import plotly.express as px

import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Your remaining code starts here...
load_dotenv()
st.set_page_config(page_title="CineMatch AI | Taste Analyzer", page_icon="🎬", layout="wide")
BACKEND_URL = "http://127.0.0.1:8000"

for key in ["selected_rec", "rec_data_cache", "analysis_cache", "show_more"]:
    if key not in st.session_state: st.session_state[key] = False if key == "show_more" else None


# ADVANCED CYBERPUNK UI ENGINE: CURSOR GLOW, CUSTOM RADAR & APP PRELOADER

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #090a0f !important; font-family: 'Plus Jakarta Sans', sans-serif !important; color: #f3f4f6 !important; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
    #stAppViewContainer::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #060709; z-index: 999999; opacity: 1; pointer-events: none; animation: fadeOutLoader 0.8s ease forwards 0.4s; }
    @keyframes fadeOutLoader { to { opacity: 0; display: none; } }
    .bg-animation { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none; background: radial-gradient(circle at var(--mouse-x, 25%) var(--mouse-y, 30%), rgba(255, 75, 75, 0.07) 0%, transparent 50%), radial-gradient(circle at 80% 70%, rgba(30, 40, 70, 0.1) 0%, transparent 60%); transition: background 0.1s linear; }
    .hero-container { text-align: center; padding: 2rem; border-radius: 20px; background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); box-shadow: 0 20px 50px rgba(0,0,0,0.4); margin-bottom: 2rem; }
    .hero-title { font-size: 2.6rem; font-weight: 800; margin-bottom: 0.5rem; background: linear-gradient(135deg, #FF4B4B 0%, #FF7676 60%, #FFFFFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .dashboard-panel { background: rgba(18, 19, 23, 0.65) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 24px; margin-bottom: 2rem; }
    
    /* ⭐ VIBRANT CORE RANKINGS (TOP 3) */
    .movie-card { padding: 18px; border-radius: 12px; margin-bottom: 12px; background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.04); border-left: 5px solid rgba(255, 75, 75, 0.4); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.2), border-color 0.3s, background 0.3s; }
    .movie-card:hover { transform: translateY(-2px) scale(1.015); background: rgba(255, 255, 255, 0.04) !important; border-left-color: #FF7676; box-shadow: 0 8px 25px rgba(255, 75, 75, 0.08); }
    
    /* 💤 FADED SUB-POOL RANKINGS (EXTENDED RECOMMENDATIONS) */
    .movie-card-faded { padding: 14px 18px; border-radius: 12px; margin-bottom: 12px; background: rgba(255, 255, 255, 0.005) !important; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.02); border-left: 5px solid rgba(148, 163, 184, 0.15); transition: transform 0.3s ease, border-color 0.3s, background 0.3s; }
    .movie-card-faded:hover { transform: translateY(-1px); background: rgba(255, 255, 255, 0.015) !important; border-left-color: #475569; }
    
    @keyframes pulse-glow { 0%, 100% { border-color: rgba(255, 75, 75, 0.4); box-shadow: 0 0 15px rgba(255, 75, 75, 0.15); } 50% { border-color: rgba(255, 118, 118, 0.8); box-shadow: 0 0 25px rgba(255, 75, 75, 0.3); } }
    .card-active { transform: scale(1.03) !important; border-left-color: #FF4B4B !important; background: linear-gradient(135deg, rgba(255, 75, 75, 0.06) 0%, rgba(14, 15, 19, 0.9) 70%) !important; animation: pulse-glow 2.5s infinite ease-in-out; }
    @keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
    .detail-panel { background: rgba(14, 15, 19, 0.85) !important; border: 1px solid rgba(255, 255, 255, 0.06); border-top: 3px solid #FF4B4B; border-radius: 14px; padding: 22px; backdrop-filter: blur(25px); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4); animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .detail-header-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 14px; margin: 12px 0; }
    .pill-tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; background: rgba(255, 75, 75, 0.1); color: #FF7676; border: 1px solid rgba(255, 75, 75, 0.2); margin-right: 6px; }
    .pill-score { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; background: rgba(255, 255, 255, 0.03); color: #e5e7eb; border: 1px solid rgba(255, 255, 255, 0.08); }
    .detail-text-body { font-size: 0.95rem; line-height: 1.55; color: #cbd5e1; background: rgba(0, 0, 0, 0.2); border-radius: 8px; padding: 12px; border: 1px solid rgba(255,255,255,0.01); }
    .sub-section-title { font-size: 0.88rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 14px 0 6px 0; display: flex; align-items: center; gap: 6px; }
    
    .stButton>button { background: linear-gradient(135deg, #FF4B4B 0%, #D32F2F 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; transition: all 0.2s ease !important; margin-top: 2px; }
    .stButton>button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 12px rgba(255, 75, 75, 0.35) !important; }
    
    /* 📉 FADED EXPANSION TOGGLE BUTTON */
    div[data-testid="stMarkdownContainer"] + div .more-rec-btn button {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.01) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        color: #94a3b8 !important;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        font-size: 0.82rem !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMarkdownContainer"] + div .more-rec-btn button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 75, 75, 0.4) !important;
        color: #fff !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.15) !important;
        transform: translateY(-1px) !important;
    }

    /* 📜 OPAQUE WRAPPER SCROLL ARCHITECTURE */
    @keyframes cascadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .scroll-box { max-height: 380px; overflow-y: auto; padding-right: 10px; margin-top: 15px; border: 1px solid rgba(255,255,255,0.02); padding: 15px; border-radius: 12px; background: rgba(5, 6, 8, 0.5); animation: cascadeIn 0.3s ease-out forwards; }
    .scroll-box::-webkit-scrollbar { width: 6px; }
    .scroll-box::-webkit-scrollbar-track { background: rgba(0,0,0,0); border-radius: 10px; }
    .scroll-box::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.05); border-radius: 10px; }
    .scroll-box::-webkit-scrollbar-thumb:hover { background: rgba(255, 75, 75, 0.2); }
</style>
<div class="bg-animation" id="ambient-canvas"></div>
<script>
    const bg = document.getElementById('ambient-canvas');
    window.addEventListener('mousemove', (e) => {
        bg.style.setProperty('--mouse-x', (e.clientX / window.innerWidth) * 100 + '%');
        bg.style.setProperty('--mouse-y', (e.clientY / window.innerHeight) * 100 + '%');
    });
</script>
""", unsafe_allow_html=True)



# HELPER DATA PIPELINE INTEGRATIONS

def map_taste_parameters(genres):
    m = {k: 10 for k in ["Adrenaline & Stakes", "Emotional Depth", "Intellectual / Plot Complexity", "Atmosphere & Escapism", "Character Realism / Grit"]}
    rules = {
        "Action": (("Adrenaline & Stakes", 50), ("Character Realism / Grit", 20)),
        "Biography": (("Character Realism / Grit", 50), ("Emotional Depth", 30)),
        "Comedy": (("Atmosphere & Escapism", 45), ("Adrenaline & Stakes", 10)),
        "Crime": (("Intellectual / Plot Complexity", 40), ("Character Realism / Grit", 45)),
        "Drama": (("Emotional Depth", 50), ("Character Realism / Grit", 30)),
        "Horror": (("Atmosphere & Escapism", 50), ("Adrenaline & Stakes", 30)),
        "Sci-Fi": (("Intellectual / Plot Complexity", 50), ("Atmosphere & Escapism", 35)),
        "Animation": (("Atmosphere & Escapism", 50), ("Emotional Depth", 25))
    }
    for g in genres:
        if g in rules:
            for dim, val in rules[g]: m[dim] += val
    return {k: min(v, 100) for k, v in m.items()}

def query_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "⚠️ Setup Error: `GEMINI_API_KEY` is missing."
    for model in ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]:
        try:
            res = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}", json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            if res.status_code == 200: return res.json()['candidates'][0]['content']['parts'][0]['text']
        except: pass
    return "🚨 Generation Cluster Timeout. Failed to fetch narrative metrics."



# APPLICATION RENDER LAYER MATRIX

st.markdown('<div class="hero-container"><h1 class="hero-title">🎬 CineMatch AI: Generative Taste Profiler</h1><p style="color: #94a3b8; margin:0; font-size:0.95rem;">Compile interactive custom narrative metrics and tracking matrices instantly.</p></div>', unsafe_allow_html=True)

genres_pool = ["Action", "Biography", "Comedy", "Crime", "Drama", "Horror", "Sci-Fi", "Animation"]
chosen_genres = st.multiselect("Configure targeted preference frameworks:", options=genres_pool, default=["Action", "Sci-Fi"])

if st.button("⚡ Execute Deep Profile Analysis", type="primary"):
    if not chosen_genres:
        st.warning("⚠️ Select at least one framework variable.")
    else:
        st.session_state.selected_rec = None 
        st.session_state.show_more = False  
        user_metrics = map_taste_parameters(chosen_genres)
        with st.spinner("✨ Mapping Taste Architectures..."):
            p_text = ", ".join([f"{k}: {v}/100" for k, v in user_metrics.items()])
            st.session_state.analysis_cache = query_gemini(f"You are a cinema psychologist. Analyze these movie preferences. Genres: {', '.join(chosen_genres)}. Metrics: {p_text}. Provide a short, clean bulleted analysis framework summarizing psychological taste drivers under 120 words total.")
        try:
            res = requests.get(f"{BACKEND_URL}/recommend", params={"genre": chosen_genres[0], "limit": 20}, timeout=10)
            if res.status_code == 200:
                data = res.json()
                
                # CUSTOM EXTENDED FALLBACK POOL WITH ENHANCED 50-100 WORD DESCRIPTIONS
                if len(data) < 20:
                    extra_fallbacks = [
                        {"movie_title": "Interstellar", "release_year": "2014", "rating": "8.7", "genre": "Sci-Fi, Drama", 
                         "description": "Set in a dystopian future where humanity is struggling to survive due to catastrophic blights and dust storms, a team of pioneering explorers and ex-NASA pilots undertake a perilous journey through a newly discovered wormhole near Saturn. Their mission is to transcend the boundaries of human space travel, navigate uncharted celestial systems, and find a habitable new home across the cosmos before Earth's ecosystem collapses entirely, leaving behind their loved ones to race against time and relativity."},
                        {"movie_title": "The Dark Knight", "release_year": "2008", "rating": "9.0", "genre": "Action, Crime", 
                         "description": "With the help of Lieutenant Jim Gordon and dedicated District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets of Gotham City. The partnership proves highly effective until their efforts are completely upended by the rise of a chaotic criminal mastermind known as the Joker. This enigmatic villain unleashes a wave of absolute anarchy upon Gotham, forcing the Caped Crusader to push his psychological and physical limits to the edge."},
                        {"movie_title": "Blade Runner 2049", "release_year": "2017", "rating": "8.0", "genre": "Sci-Fi, Action", 
                         "description": "Thirty years after the complex events of the original investigation, a new blade runner and LAPD Officer named K unearths a long-buried, deeply guarded secret that holds the dangerous potential to plunge what remains of an unstable society into absolute chaos. This paradigm-shifting discovery leads K on an existential quest to find Rick Deckard, a former LAPD blade runner who has been missing from civilization for three decades, forcing him to question his own synthetic reality."},
                        {"movie_title": "Spiderman: Into the Spiderverse", "release_year": "2018", "rating": "8.4", "genre": "Animation, Action", 
                         "description": "Brooklyn teenager Miles Morales is struggling to adapt to his new high school and live up to the expectations of his parents when he is suddenly bitten by a radioactive spider, gaining extraordinary powers. After witnessing the tragic death of his universe's Peter Parker, Miles must step up to stop a reality-threatening particle collider built by the Kingpin. Along the way, he crosses paths with alternate-dimension spider-heroes, learning the true, isolating responsibility of wearing the iconic mask."},
                        {"movie_title": "Inception", "release_year": "2010", "rating": "8.8", "genre": "Sci-Fi, Action", 
                         "description": "Dom Cobb is a highly skilled thief who specializes in extraction, the dangerous art of stealing valuable corporate secrets from deep within the subconscious minds of targets while they are in a vulnerable dream state. His rare talent has made him a coveted asset in the world of corporate espionage, but it has also made him an international fugitive. To win his life back, he must successfully pull off inception—planting an idea instead of stealing one."},
                        {"movie_title": "The Matrix", "release_year": "1999", "rating": "8.7", "genre": "Sci-Fi, Action", 
                         "description": "Thomas Anderson is a disillusioned computer programmer who moonlights as a notorious hacker under the alias Neo. His mundane perception of life is permanently shattered when he is contacted by mysterious subterranean rebels led by the enigmatic Morpheus. They reveal a terrifying truth: the reality he knows is actually an elaborate, simulated simulation called the Matrix, built by malicious artificial intelligence to subjugate human bodies as a bio-electric energy source, launching him into a war for freedom."},
                        {"movie_title": "Gladiator", "release_year": "2000", "rating": "8.5", "genre": "Action, Adventure, Drama", 
                         "description": "Once a highly respected and victorious Roman General who led his legions with absolute honor, Maximus Decimus Meridius is betrayed by Commodus, the corrupt and ambitious son of the Emperor Marcus Aurelius. After his family is brutally murdered, Maximus narrowly escapes death only to be captured and forced into slavery as a gladiator. Driven by a burning desire for vengeance, he rises through the ranks of the Colosseum arena, capturing the hearts of the public to challenge the throne."},
                        {"movie_title": "The Prestige", "release_year": "2006", "rating": "8.5", "genre": "Drama, Mystery, Sci-Fi", 
                         "description": "In the vibrant, competitive theatrical world of late 19th-century London, two exceptionally talented stage magicians, Robert Angier and Alfred Borden, start as friends and colleagues. However, when a sudden onstage illusion ends in a horrific, fatal accident, a bitter enmity is born between them. Their professional rivalry quickly devolves into an obsessive, life-consuming psychological war filled with deceit, as both men sacrifice their relationships, sanity, and humanity to create the ultimate illusion."},
                        {"movie_title": "Whiplash", "release_year": "2014", "rating": "8.5", "genre": "Drama, Music", 
                         "description": "Andrew Neiman is an ambitious, young jazz drummer who is intensely determined to rise to the absolute peak of his elite elite music conservatory. Haunted by his father's failed writing career, Andrew practices until his hands literally bleed. His talent catches the attention of Terence Fletcher, an infamous instructor known just as much for his terrifying, abusive teaching methods as his musical genius. Andrew enters a grueling psychological crucible where his sanity is pushed to the edge."},
                        {"movie_title": "The Departure", "release_year": "2017", "rating": "7.9", "genre": "Drama", 
                         "description": "This poignant, contemplative piece takes a profound psychological look into the weight of human choice and its long-term ethical consequences. The narrative follows an individual navigating an unexpected structural crossroads where personal ambitions collide directly with deep-seated social responsibilities. Through a series of quiet, emotional confrontations, the story examines the fragile nature of memory, how we justify our life departures, and the lasting impressions left on the communities we choose to leave behind."}
                    ]
                    for item in extra_fallbacks:
                        if len(data) >= 20: break
                        if item["movie_title"] not in [m["movie_title"] for m in data]:
                            data.append(item)
                st.session_state.rec_data_cache = data
            else:
                st.session_state.rec_data_cache = []
        except requests.exceptions.ConnectionError:
            st.session_state.rec_data_cache = "connection_error"

if st.session_state.analysis_cache:
    user_metrics = map_taste_parameters(chosen_genres)
    st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
    top_l, top_r = st.columns([52, 48], gap="large")
    with top_l:
        st.markdown("#### 🧠 User Movie Taste Profile Summary")
        st.markdown(st.session_state.analysis_cache)
    with top_r:
        st.markdown("<h4 style='margin:0 0 10px 0;'>📊 Parametric Vector Distribution Mapping</h4>", unsafe_allow_html=True)
        fig = px.line_polar(pd.DataFrame({'Dim': list(user_metrics.keys()), 'Val': list(user_metrics.values())}), r='Val', theta='Dim', line_close=True, range_r=[0, 100], color_discrete_sequence=['#FF4B4B'])
        fig.update_traces(fill='toself', fillcolor='rgba(255, 75, 75, 0.2)', line=dict(width=3, color='#FF4B4B'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, showticklabels=False, gridcolor='rgba(255,255,255,0.08)', linecolor='rgba(0,0,0,0)'), angularaxis=dict(gridcolor='rgba(255,255,255,0.08)', color='#94a3b8', tickfont=dict(size=10, family='Plus Jakarta Sans')), bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=240, margin=dict(l=45, r=45, t=15, b=15))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🎬 Custom-Tailored Cinematic Match Rankings")
    if st.session_state.rec_data_cache == "connection_error":
        st.error("🚨 Connection dropped: Validate if backend cluster `server.py` is operational on Port 8000.")
    elif not st.session_state.rec_data_cache:
        st.info("No matching records found inside current database architecture.")
    else:
        primary_display_pool = st.session_state.rec_data_cache[:3]
        extended_overflow_pool = st.session_state.rec_data_cache[3:20]
        
        btm_l, btm_r = st.columns([45, 55], gap="large")
        with btm_l:
            st.caption("💡 Select a movie card below to populate tracking parameters:")
            
            # Display primary baseline rankings (Top 3 Premium Cards)
            for idx, item in enumerate(primary_display_pool, 1):
                rec_id = f"movie_{idx}"
                card_class = "movie-card card-active" if (st.session_state.selected_rec == rec_id) else "movie-card"
                st.markdown(f'<div class="{card_class}"><h4 style="margin:0 0 4px 0; color:#fff;">#{idx} {item["movie_title"]} <span style="font-size:0.85rem; color:#64748b;">({item["release_year"]})</span></h4><p style="margin:0; font-size:0.88rem; color:#94a3b8;">⭐ Rating: <b style="color:#fff;">{item["rating"]}/10</b> | <span>{item["genre"]}</span></p></div>', unsafe_allow_html=True)
                if st.button(f"Inspect Analysis #{idx}", key=f"btn_{rec_id}", use_container_width=True):
                    st.session_state.selected_rec = rec_id
                    st.rerun()
                    
            # Isolated Faded Action Toggle Button Frame
            if extended_overflow_pool:
                st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                btn_label = "Show Less Recommendations" if st.session_state.show_more else "Discover More Recommendations"
                
                st.markdown('<div class="more-rec-btn">', unsafe_allow_html=True)
                if st.button(btn_label, key="toggle_overflow_pool", use_container_width=True):
                    st.session_state.show_more = not st.session_state.show_more
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Render hidden extended pool items with muted/faded profiles
                if st.session_state.show_more:
                    st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
                    for ex_idx, item in enumerate(extended_overflow_pool, len(primary_display_pool) + 1):
                        rec_id = f"movie_{ex_idx}"
                        card_class = "movie-card card-active" if (st.session_state.selected_rec == rec_id) else "movie-card-faded"
                        st.markdown(f'<div class="{card_class}"><h4 style="margin:0 0 4px 0; color:#cbd5e1;">#{ex_idx} {item["movie_title"]} <span style="font-size:0.82rem; color:#475569;">({item["release_year"]})</span></h4><p style="margin:0; font-size:0.84rem; color:#64748b;">⭐ Rating: <b style="color:#94a3b8;">{item["rating"]}/10</b> | <span style="color:#475569;">{item["genre"]}</span></p></div>', unsafe_allow_html=True)
                        if st.button(f"Inspect Analysis #{ex_idx}", key=f"btn_{rec_id}", use_container_width=True):
                            st.session_state.selected_rec = rec_id
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

        with btm_r:
            if st.session_state.selected_rec:
                active_idx = int(st.session_state.selected_rec.split("_")[1]) - 1
                active_match = st.session_state.rec_data_cache[active_idx]
                st.markdown('<div class="detail-panel"><h3 style="margin:0; color:#fff; font-weight:800; font-size:1.3rem;">📊 Movie / Series Details ::</h3>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-header-card"><h4 style="margin:0 0 8px 0; color:#FF7676; font-size:1.1rem;">{active_match["movie_title"]}</h4><span class="pill-tag">🎭 Context: {active_match["genre"]}</span><span class="pill-score">⭐ Alignment: {active_match["rating"]}/10</span></div>', unsafe_allow_html=True)
                
                # MOVIE DESCRIPTION FIELD (Now holds detailed narrative block text 50-100 words)
                st.markdown('<div class="sub-section-title">📝 Core Movie Description:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-text-body">{active_match.get("description", "No contextual description available.")}</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="sub-section-title">🧠 AI Sentiment Analysis:</div>', unsafe_allow_html=True)
                with st.spinner("Analyzing narrative vector architectures..."):
                    deep_insights = query_gemini(
                        f"Provide a comprehensive cinema psychology breakdown of '{active_match['movie_title']}' within the genre framework of '{active_match['genre']}'. "
                        f"Analyze its narrative setup, psychological emotional undertones, and character driver mechanisms. "
                        f"Your entire response MUST be structural, highly insightful, and strictly between 50 and 100 words long."
                    )
                st.markdown(f'<div class="detail-text-body">{deep_insights}</div><div style="margin-bottom: 14px;"></div>', unsafe_allow_html=True)
                
                if st.button("Close Detailed Inspection Panel ✕", use_container_width=True):
                    st.session_state.selected_rec = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("<div style='border: 2px dashed rgba(255,255,255,0.04); border-radius:14px; padding:65px 20px; text-align:center; min-height: 240px; display: flex; flex-direction: column; justify-content: center;'><p style='color:#64748b; margin:0;'>👈 Select a cinematic match tracking card on the left to unpack deep feature vectors instantly.</p></div>", unsafe_allow_html=True)
