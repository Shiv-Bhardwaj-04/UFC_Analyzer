"""
UFC Analytics Dashboard — Main Application
Professional MMA Statistics & ML Platform
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.config.settings import APP_TITLE, APP_ICON, PAGE_LAYOUT
from src.utils.data_loader import load_fighters_data, load_events_data
from src.utils.search import FighterSearch
from src.pages import home, fighter_search, events, compare, rankings

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# ── Global CSS — Dark Premium Theme ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Base */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #080810 !important;
    font-family: 'Inter', sans-serif !important;
    color: #e0e0e0 !important;
}

[data-testid="stSidebar"] {
    background: #0d0d1a !important;
    border-right: 1px solid #1e1e2e !important;
}

/* Remove default Streamlit padding */
.block-container { padding-top: 1.5rem !important; }

/* Headers */
h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; }

/* Page hero */
.page-hero { text-align: center; padding: 2rem 0 1.5rem; }
.page-title {
    font-size: 2.8rem; font-weight: 900; letter-spacing: 2px;
    background: linear-gradient(135deg, #d62728, #ff6b6b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0;
}
.page-subtitle { color: #777; font-size: 1rem; margin-top: 0.5rem; }

/* Info box */
.info-box {
    background: #0d0d1a;
    border-left: 4px solid #d62728;
    border: 1px solid #1e1e2e;
    border-left: 4px solid #d62728;
    padding: 1rem 1.25rem;
    border-radius: 10px;
    margin: 1rem 0;
    color: #bbb;
}
.info-box strong { color: #e0e0e0; }

/* Suggestion box */
.suggestion-box {
    background: #1a1500;
    border-left: 4px solid #f39c12;
    border: 1px solid #2e2a0a;
    border-left: 4px solid #f39c12;
    padding: 1rem 1.25rem;
    border-radius: 10px;
    margin: 1rem 0;
}

/* ML stat card */
.ml-stat-card {
    background: #0d0d1a;
    border: 1.5px solid #d6272840;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.ml-stat-value { font-size: 2rem; font-weight: 900; color: #d62728; }
.ml-stat-label { color: #777; font-size: 0.8rem; margin-top: 0.2rem; }

/* Fighter select label */
.fighter-select-label {
    font-weight: 700; font-size: 1rem; color: #ccc;
    margin-bottom: 0.4rem;
}

/* Streamlit buttons */
.stButton > button {
    background: linear-gradient(135deg, #d62728, #c0392b) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #e74c3c, #d62728) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px #d6272840 !important;
}

/* Sidebar nav radio */
[data-testid="stRadio"] label { color: #ccc !important; }
[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    border-color: #d62728 !important;
    background-color: #d62728 !important;
}

/* Tabs */
[data-baseweb="tab"] { color: #888 !important; }
[data-baseweb="tab"][aria-selected="true"] {
    color: #d62728 !important;
    border-bottom-color: #d62728 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid #1e1e2e; border-radius: 8px; }

/* Expander */
[data-testid="stExpander"] {
    background: #0d0d1a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background: #0d0d1a !important;
    border-color: #2e2e3e !important;
    color: #e0e0e0 !important;
}

/* Text input */
[data-baseweb="input"] > div {
    background: #0d0d1a !important;
    border-color: #2e2e3e !important;
    color: #e0e0e0 !important;
}

/* Spinner */
[data-testid="stSpinner"] { color: #d62728 !important; }

/* Success/Warning/Error banners */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* Metric */
[data-testid="metric-container"] {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 1rem;
}

/* Divider */
hr { border-color: #1e1e2e !important; }

/* Slider */
[data-baseweb="slider"] [data-testid="stSlider"] { color: #d62728 !important; }

/* Sidebar brand */
.sidebar-brand {
    text-align: center;
    padding: 1rem 0 0.5rem;
}
.sidebar-brand-title {
    font-size: 1.4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #d62728, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-brand-sub {
    font-size: 0.72rem;
    color: #555;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* Nav section labels */
.nav-section-label {
    font-size: 0.68rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    padding: 0.5rem 0 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Load data + ML models ─────────────────────────────────────────────────────
@st.cache_resource
def initialize_app():
    fighters_df = load_fighters_data()
    events_df   = load_events_data()
    search_engine = FighterSearch(fighters_df)
    return fighters_df, events_df, search_engine

@st.cache_resource
def initialize_ml(fighters_df):
    """Initialize and train all ML models once."""
    try:
        from src.ml.fight_predictor import FightPredictor
        from src.ml.similar_fighters import FighterSimilarity
        from src.ml.fighter_clustering import load_and_cluster

        predictor = FightPredictor()
        predictor.train()

        similarity = FighterSimilarity()
        similarity.train(fighters_df)

        clustered_df = load_and_cluster()

        return predictor, similarity, clustered_df
    except Exception as e:
        st.sidebar.error(f"ML init error: {e}")
        return None, None, None

fighters_df, events_df, search_engine = initialize_app()
predictor, similarity_engine, clustered_df = initialize_ml(fighters_df)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div style='font-size: 2.5rem;'>🥊</div>
        <div class='sidebar-brand-title'>UFC ANALYTICS</div>
        <div class='sidebar-brand-sub'>ML-Powered Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='nav-section-label'>📊 Analytics</div>", unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔍 Fighter Search", "📅 Events", "⚔️ Compare", "🏆 Rankings"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='nav-section-label'>🤖 Machine Learning</div>", unsafe_allow_html=True)
    ml_page = st.radio(
        "ML Navigation",
        ["── Select ML Tool ──", "🤖 Fight Predictor", "🧬 Fighter DNA", "🔗 Similar Fighters"],
        label_visibility="collapsed"
    )

    # Dataset info
    st.markdown("---")
    st.markdown(f"""
    <div style='background: #0d0d1a; border: 1px solid #1e1e2e; border-radius: 10px; padding: 1rem;'>
        <div style='font-size: 0.7rem; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;'>Dataset</div>
        <div style='color: #ccc; font-size: 0.82rem;'>
            🥊 <b style='color:#d62728'>{len(fighters_df):,}</b> fighters<br>
            📅 <b style='color:#3498db'>{events_df["Event Name"].nunique():,}</b> events<br>
            ⚔️ <b style='color:#2ecc71'>{len(events_df):,}</b> fights<br>
            📆 <span style='color:#888'>1994 – 2023</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ML status
    ml_ready = predictor is not None and predictor.trained
    st.markdown(f"""
    <div style='margin-top: 0.75rem; background: #0d0d1a; border: 1px solid #1e1e2e;
                border-radius: 10px; padding: 1rem;'>
        <div style='font-size: 0.7rem; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;'>ML Status</div>
        <div style='font-size: 0.82rem; color: #ccc;'>
            {'✅' if ml_ready else '⏳'} Fight Predictor
            {'<span style="color:#2ecc71">Ready</span>' if ml_ready else '<span style="color:#888">Loading</span>'}<br>
            {'✅' if clustered_df is not None else '⏳'} Fighter DNA
            {'<span style="color:#2ecc71">Ready</span>' if clustered_df is not None else '<span style="color:#888">Loading</span>'}<br>
            {'✅' if similarity_engine is not None and similarity_engine.trained else '⏳'} Similarity Engine
            {'<span style="color:#2ecc71">Ready</span>' if similarity_engine is not None and similarity_engine.trained else '<span style="color:#888">Loading</span>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top: 1rem; text-align: center;'>
        <div style='font-size: 0.7rem; color: #444;'>Built with Streamlit · scikit-learn · Plotly</div>
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────────────────
# ML pages take priority if a real ML tool is selected
if ml_page != "── Select ML Tool ──":
    if ml_page == "🤖 Fight Predictor":
        from src.pages import predictor as pred_page
        pred_page.render(fighters_df, predictor)
    elif ml_page == "🧬 Fighter DNA":
        from src.pages import clustering as clust_page
        clust_page.render(fighters_df, clustered_df)
    elif ml_page == "🔗 Similar Fighters":
        from src.pages import similar_fighters as sim_page
        sim_page.render(fighters_df, similarity_engine)
else:
    if page == "🏠 Home":
        home.render(fighters_df, events_df)
    elif page == "🔍 Fighter Search":
        fighter_search.render(fighters_df, search_engine)
    elif page == "📅 Events":
        events.render(events_df)
    elif page == "⚔️ Compare":
        compare.render(fighters_df)
    else:
        rankings.render(fighters_df)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #444; font-size: 0.78rem; padding: 1rem 0;'>
    <span style='color: #d62728; font-weight: 700;'>🥊 UFC Analytics Dashboard</span>
    &nbsp;·&nbsp; ML-Powered MMA Statistics Platform
    &nbsp;·&nbsp; Random Forest · K-Means · KNN
</div>
""", unsafe_allow_html=True)
