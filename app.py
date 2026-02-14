"""
UFC Analytics Dashboard - Main Application
Professional MMA Statistics Analysis Platform
"""
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.config.settings import APP_TITLE, APP_ICON, PAGE_LAYOUT
from src.utils.data_loader import load_fighters_data, load_events_data
from src.utils.search import FighterSearch
from src.pages import home, fighter_search, events, compare, rankings

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #d62728;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #d62728;
        margin: 1rem 0;
    }
    .suggestion-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_resource
def initialize_app():
    """Initialize application and load data"""
    fighters_df = load_fighters_data()
    events_df = load_events_data()
    search_engine = FighterSearch(fighters_df)
    return fighters_df, events_df, search_engine

fighters_df, events_df, search_engine = initialize_app()

# Sidebar
with st.sidebar:
    st.markdown(f"<h1 style='text-align: center; color: #d62728;'>{APP_ICON} UFC Analytics</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # About Section
    with st.expander("ℹ️ About This App", expanded=False):
        st.markdown(f"""
        **{APP_TITLE}** is a professional MMA statistics analysis platform.
        
        **Features:**
        - 📊 Advanced fighter analytics
        - 📈 Interactive visualizations
        - ⚔️ Head-to-head comparisons
        - 🏆 Comprehensive rankings
        - 📅 Event-level insights
        - 🔍 Smart search with AI-powered matching
        
        **Data:**
        - **Fighters:** {len(fighters_df):,}
        - **Events:** {events_df['Event Name'].nunique():,}
        - **Total Fights:** {len(events_df):,}
        
        **Search Capabilities:**
        - ✅ First name matching
        - ✅ Last name matching
        - ✅ Nickname matching
        - ✅ Fuzzy matching (handles typos)
        - ✅ Partial matching
        - ✅ Multi-word search
        """)
    
    # Features
    with st.expander("🎯 Key Features", expanded=False):
        st.markdown("""
        **1. Home Dashboard**
        - Statistical overview
        - Weight class analysis
        - Performance distributions
        
        **2. Fighter Search**
        - Multi-strategy search engine
        - Autocomplete suggestions
        - Detailed fighter profiles
        - Performance metrics
        
        **3. Event Analysis**
        - Historical event data
        - Fight breakdowns
        - Method analysis
        
        **4. Fighter Comparison**
        - Side-by-side stats
        - Visual comparisons
        - Record analysis
        
        **5. Rankings**
        - Most wins
        - Best win rates
        - Most active fighters
        """)
    
    # How to Use
    with st.expander("📖 User Guide", expanded=False):
        st.markdown("""
        **Search Tips:**
        
        The search engine uses multiple strategies:
        
        1. **Exact Match**: Type exact first/last name
           - Example: "Conor" or "McGregor"
        
        2. **Nickname Search**: Use fighter nicknames
           - Example: "Notorious" → Conor McGregor
        
        3. **Partial Match**: Type part of name
           - Example: "Jon" → Jon Jones
        
        4. **Fuzzy Match**: Handles typos
           - Example: "Mcgreggor" → McGregor
        
        5. **Multi-word**: Search full names
           - Example: "Conor McGregor"
        
        **Navigation:**
        - Use sidebar to switch pages
        - Hover over charts for details
        - Click expandable sections
        """)
    
    st.markdown("---")
    st.markdown("### 📍 Navigation")
    
    page = st.radio(
        "Select a page:",
        ["🏠 Home", "🔍 Fighter Search", "📅 Events", "⚔️ Compare", "🏆 Rankings"],
        label_visibility="collapsed"
    )

# Route to pages
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

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style='text-align: center; color: #666;'>
        <p><strong>{APP_ICON} {APP_TITLE}</strong></p>
        <p>Professional MMA Statistics Platform</p>
        <p style='font-size: 0.8rem;'>Built with Streamlit • Plotly • Python</p>
    </div>
    """, unsafe_allow_html=True)
