"""
Rankings Page
"""
import streamlit as st
from src.components.ui_components import page_header
from src.config.settings import MIN_FIGHTS_FOR_WINRATE


def render(fighters_df):
    """Render rankings page"""
    page_header("🏆 RECORDS & RANKINGS", "Top fighters across different categories")
    
    st.markdown("""
    <div class='info-box'>
        <p>🏆 <strong>Explore rankings</strong> based on wins, win rate, and activity level.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🥇 Most Wins", "📈 Best Win Rate", "🔥 Most Active"])
    
    with tab1:
        st.markdown("### 🥇 Top 20 Fighters with Most Wins")
        top_wins = fighters_df.nlargest(20, 'Wins')[
            ['First Name', 'Last Name', 'Nickname', 'Wins', 'Losses', 'Draws', 'Weight', 'Win Rate']
        ]
        top_wins['Record'] = top_wins['Wins'].astype(str) + '-' + top_wins['Losses'].astype(str) + '-' + top_wins['Draws'].astype(str)
        st.dataframe(top_wins, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown(f"### 📈 Top 20 Fighters by Win Rate (Minimum {MIN_FIGHTS_FOR_WINRATE} fights)")
        qualified = fighters_df[fighters_df['Total Fights'] >= MIN_FIGHTS_FOR_WINRATE].nlargest(20, 'Win Rate')
        qualified = qualified[['First Name', 'Last Name', 'Nickname', 'Wins', 'Losses', 'Win Rate', 'Total Fights', 'Weight']]
        st.dataframe(qualified, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 🔥 Top 20 Most Active Fighters")
        most_active = fighters_df.nlargest(20, 'Total Fights')[
            ['First Name', 'Last Name', 'Nickname', 'Total Fights', 'Wins', 'Losses', 'Win Rate', 'Weight']
        ]
        st.dataframe(most_active, use_container_width=True, hide_index=True)
