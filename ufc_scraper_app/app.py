from pathlib import Path
import pandas as pd
import requests
import streamlit as st
import pickle
from scrapers import write_fighters_csv, write_events_csv
from ml_models import UFCFightPredictor, UFCQuestionAnswering


st.set_page_config(
    page_title="UFC Fight Predictor & Analytics",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
FIGHTERS_CSV = DATA_DIR / "ufc_fighters.csv"
EVENTS_CSV = DATA_DIR / "ufc_event_data.csv"
MODEL_PATH = DATA_DIR / "ufc_model.pkl"


@st.cache_resource
def load_model():
    """Load or train the ML model"""
    if MODEL_PATH.exists() and FIGHTERS_CSV.exists() and EVENTS_CSV.exists():
        predictor = UFCFightPredictor()
        predictor.load_model(MODEL_PATH)
        return predictor
    return None


@st.cache_data
def load_data():
    """Load fighter and event data"""
    if FIGHTERS_CSV.exists() and EVENTS_CSV.exists():
        fighters = pd.read_csv(FIGHTERS_CSV)
        events = pd.read_csv(EVENTS_CSV)
        return fighters, events
    return None, None


def train_model_page():
    """Model training interface"""
    st.title("🤖 Train ML Model")
    st.markdown("Train the fight prediction model on UFC historical data")
    
    if not FIGHTERS_CSV.exists() or not EVENTS_CSV.exists():
        st.warning("⚠️ Please scrape data first before training the model!")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fighters Data", f"{len(pd.read_csv(FIGHTERS_CSV)):,} fighters")
    with col2:
        st.metric("Events Data", f"{len(pd.read_csv(EVENTS_CSV)):,} fights")
    
    if st.button("🚀 Train Model", type="primary", use_container_width=True):
        with st.spinner("Training model... This may take a few minutes"):
            try:
                predictor = UFCFightPredictor()
                accuracy, report = predictor.train(str(EVENTS_CSV), str(FIGHTERS_CSV))
                predictor.save_model(str(MODEL_PATH))
                
                st.success(f"✅ Model trained successfully! Accuracy: {accuracy:.2%}")
                st.text("Classification Report:")
                st.code(report)
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Training failed: {e}")


def prediction_page():
    """Fight prediction interface"""
    st.title("🥊 UFC Fight Predictor")
    st.markdown("Predict fight outcomes using machine learning")
    
    predictor = load_model()
    fighters_df, _ = load_data()
    
    if predictor is None or not predictor.is_trained:
        st.warning("⚠️ Model not trained yet! Please train the model first.")
        return
    
    if fighters_df is None:
        st.error("❌ Fighter data not available!")
        return
    
    st.subheader("Select Fighters")
    
    col1, col2 = st.columns(2)
    
    fighters_df['full_name'] = fighters_df['First Name'] + ' ' + fighters_df['Last Name']
    fighter_names = sorted(fighters_df['full_name'].unique())
    
    with col1:
        st.markdown("### 🔴 Fighter 1")
        fighter1_name = st.selectbox("Select Fighter 1", fighter_names, key="f1")
        fighter1_data = fighters_df[fighters_df['full_name'] == fighter1_name].iloc[0]
        
        st.write(f"**Record:** {fighter1_data['Wins']}-{fighter1_data['Losses']}-{fighter1_data['Draws']}")
        st.write(f"**Height:** {fighter1_data['Height']}")
        st.write(f"**Reach:** {fighter1_data['Reach']}")
        st.write(f"**Weight:** {fighter1_data['Weight']}")
    
    with col2:
        st.markdown("### 🔵 Fighter 2")
        fighter2_name = st.selectbox("Select Fighter 2", fighter_names, key="f2")
        fighter2_data = fighters_df[fighters_df['full_name'] == fighter2_name].iloc[0]
        
        st.write(f"**Record:** {fighter2_data['Wins']}-{fighter2_data['Losses']}-{fighter2_data['Draws']}")
        st.write(f"**Height:** {fighter2_data['Height']}")
        st.write(f"**Reach:** {fighter2_data['Reach']}")
        st.write(f"**Weight:** {fighter2_data['Weight']}")
    
    weight_class = st.selectbox("Weight Class", [
        "Flyweight", "Bantamweight", "Featherweight", "Lightweight",
        "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"
    ])
    
    if st.button("🎯 Predict Winner", type="primary", use_container_width=True):
        # Prepare fighter stats
        def parse_height(h):
            if pd.isna(h) or '--' in str(h):
                return 0
            try:
                parts = str(h).replace('"', '').replace("'", ' ').split()
                return int(parts[0]) * 12 + int(parts[1]) if len(parts) == 2 else 0
            except:
                return 0
        
        def parse_reach(r):
            if pd.isna(r) or '--' in str(r):
                return 0
            return float(str(r).replace('"', ''))
        
        def parse_weight(w):
            if pd.isna(w) or '--' in str(w):
                return 0
            return float(str(w).replace(' lbs.', ''))
        
        f1_stats = {
            'height': parse_height(fighter1_data['Height']),
            'reach': parse_reach(fighter1_data['Reach']),
            'weight': parse_weight(fighter1_data['Weight']),
            'wins': int(fighter1_data['Wins']),
            'losses': int(fighter1_data['Losses']),
            'total_fights': int(fighter1_data['Wins']) + int(fighter1_data['Losses']) + int(fighter1_data['Draws']),
            'win_rate': int(fighter1_data['Wins']) / (int(fighter1_data['Wins']) + int(fighter1_data['Losses']) + int(fighter1_data['Draws'])) if (int(fighter1_data['Wins']) + int(fighter1_data['Losses']) + int(fighter1_data['Draws'])) > 0 else 0
        }
        
        f2_stats = {
            'height': parse_height(fighter2_data['Height']),
            'reach': parse_reach(fighter2_data['Reach']),
            'weight': parse_weight(fighter2_data['Weight']),
            'wins': int(fighter2_data['Wins']),
            'losses': int(fighter2_data['Losses']),
            'total_fights': int(fighter2_data['Wins']) + int(fighter2_data['Losses']) + int(fighter2_data['Draws']),
            'win_rate': int(fighter2_data['Wins']) / (int(fighter2_data['Wins']) + int(fighter2_data['Losses']) + int(fighter2_data['Draws'])) if (int(fighter2_data['Wins']) + int(fighter2_data['Losses']) + int(fighter2_data['Draws'])) > 0 else 0
        }
        
        result = predictor.predict_fight(f1_stats, f2_stats, weight_class)
        
        st.markdown("---")
        st.markdown("## 🏆 Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Fighter 1 Win Probability", f"{result['fighter1_win_prob']:.1f}%")
        
        with col2:
            winner_name = fighter1_name if result['winner'] == 'Fighter 1' else fighter2_name
            st.metric("Predicted Winner", winner_name)
        
        with col3:
            st.metric("Fighter 2 Win Probability", f"{result['fighter2_win_prob']:.1f}%")
        
        st.progress(result['fighter1_win_prob'] / 100)
        st.markdown(f"**Confidence Level:** {result['confidence']:.1f}%")


def qa_page():
    """Question answering interface"""
    st.title("💬 Ask About UFC Data")
    st.markdown("Ask questions about fighters, fights, and statistics")
    
    fighters_df, events_df = load_data()
    
    if fighters_df is None or events_df is None:
        st.warning("⚠️ Please scrape data first!")
        return
    
    qa_system = UFCQuestionAnswering(fighters_df, events_df)
    
    st.markdown("### 💡 Example Questions:")
    examples = st.columns(3)
    with examples[0]:
        if st.button("Who has the most wins?"):
            st.session_state.question = "Who has the most wins?"
    with examples[1]:
        if st.button("Top 10 fighters"):
            st.session_state.question = "List top 10 fighters by wins"
    with examples[2]:
        if st.button("Weight classes"):
            st.session_state.question = "What are the most common weight classes?"
    
    question = st.text_input(
        "Ask your question:",
        value=st.session_state.get('question', ''),
        placeholder="e.g., Who has the highest win rate?"
    )
    
    if st.button("🔍 Get Answer", type="primary") or question:
        if question:
            result = qa_system.answer_question(question)
            
            if result['type'] == 'error':
                st.error(result['message'])
                if 'suggestions' in result:
                    st.info("**Try these questions:**")
                    for sugg in result['suggestions']:
                        st.write(f"• {sugg}")
            
            elif result['type'] == 'answer':
                st.success(result['message'])
                if result['data'] is not None:
                    if isinstance(result['data'], pd.DataFrame):
                        st.dataframe(result['data'], use_container_width=True)
                    elif isinstance(result['data'], dict):
                        for key, value in result['data'].items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.write(result['data'])
            
            else:
                st.info(result['message'])
                if 'suggestions' in result:
                    for sugg in result['suggestions']:
                        st.write(f"• {sugg}")


def scraper_page():
    """Data scraping interface"""
    st.title("📊 Data Scraper")
    st.markdown("Scrape fighter and event data from UFC Stats")
    
    left, right = st.columns(2)
    
    with left:
        st.subheader("👤 Fighters")
        if st.button("Scrape Fighters", use_container_width=True, type="primary"):
            try:
                with st.spinner("Scraping fighters..."):
                    write_fighters_csv(str(FIGHTERS_CSV))
                st.success(f"✅ Saved {FIGHTERS_CSV.name}")
                st.rerun()
            except Exception as exc:
                st.error(f"❌ Failed: {exc}")
    
    with right:
        st.subheader("🎯 Events")
        if st.button("Scrape Events", use_container_width=True, type="primary"):
            try:
                with st.spinner("Scraping events..."):
                    write_events_csv(str(EVENTS_CSV))
                st.success(f"✅ Saved {EVENTS_CSV.name}")
                st.rerun()
            except Exception as exc:
                st.error(f"❌ Failed: {exc}")
    
    st.divider()
    
    if FIGHTERS_CSV.exists():
        df = pd.read_csv(FIGHTERS_CSV)
        st.subheader("👤 Fighters Preview")
        st.dataframe(df.head(20), use_container_width=True)
    
    if EVENTS_CSV.exists():
        df = pd.read_csv(EVENTS_CSV)
        st.subheader("🎯 Events Preview")
        st.dataframe(df.head(20), use_container_width=True)


def main():
    st.sidebar.title("🥊 UFC Analytics")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Data Scraper", "🤖 Train Model", "🥊 Fight Predictor", "💬 Ask Questions"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**How to use:**\n"
        "1. Scrape data from UFC Stats\n"
        "2. Train the ML model\n"
        "3. Predict fight outcomes\n"
        "4. Ask questions about UFC data"
    )
    
    if page == "📊 Data Scraper":
        scraper_page()
    elif page == "🤖 Train Model":
        train_model_page()
    elif page == "🥊 Fight Predictor":
        prediction_page()
    elif page == "💬 Ask Questions":
        qa_page()


if __name__ == "__main__":
    main()
