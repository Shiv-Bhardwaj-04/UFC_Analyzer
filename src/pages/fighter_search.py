"""
Fighter Search Page with Advanced Search Engine
"""
import streamlit as st
from src.components.ui_components import page_header, fighter_card, suggestion_box


def render(fighters_df, search_engine):
    """Render fighter search page"""
    page_header("🔍 FIGHTER SEARCH", "Advanced search with multi-strategy matching")
    
    # Search info
    st.markdown("""
    <div class='info-box'>
        <p>🔍 <strong>Smart Search Engine:</strong> Search by first name, last name, or nickname. Handles typos and partial matches!</p>
        <p><strong>Examples:</strong> "Conor", "McGregor", "Notorious", "Jon Jones", "Silva", etc.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search methods
    col1, col2 = st.columns([3, 1])
    
    with col2:
        search_method = st.radio(
            "Search Method:",
            ["🔍 Smart Search", "📋 Dropdown"],
            label_visibility="visible"
        )
    
    with col1:
        if search_method == "🔍 Smart Search":
            query = st.text_input(
                "Type fighter name (first, last, or nickname)",
                placeholder="e.g., Conor, McGregor, Notorious, Jon Jones...",
                key="smart_search"
            )
            
            if query:
                with st.spinner("Searching..."):
                    results = search_engine.search(query, max_results=10)
                
                if len(results) > 0:
                    st.success(f"✅ Found {len(results)} fighter(s) matching '{query}'")
                    
                    for idx, fighter in results.iterrows():
                        with st.expander(
                            f"🥊 {fighter['First Name']} {fighter['Last Name']} - '{fighter['Nickname']}'",
                            expanded=(idx == results.index[0])
                        ):
                            fighter_card(fighter)
                else:
                    st.warning(f"⚠️ No fighters found for '{query}'")
                    
                    # Show suggestions
                    suggestions = search_engine.get_suggestions(query, n=5)
                    if suggestions:
                        st.markdown("""
                        <div class='suggestion-box'>
                            <h4>💡 Did you mean?</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for suggestion in suggestions:
                            if st.button(f"👉 {suggestion.title()}", key=f"suggest_{suggestion}"):
                                st.session_state.smart_search = suggestion
                                st.rerun()
                    
                    # Tips
                    st.info("""
                    **Search Tips:**
                    - Try searching by first name only (e.g., "Conor")
                    - Try searching by last name only (e.g., "McGregor")
                    - Try the fighter's nickname (e.g., "Notorious")
                    - Use the dropdown method below for browsing
                    """)
            else:
                st.info("👆 Enter a fighter name to search")
        
        else:
            # Dropdown search
            fighter_names = [''] + sorted(fighters_df['Full Name'].tolist())
            selected = st.selectbox(
                "Select fighter from list",
                options=fighter_names,
                format_func=lambda x: "-- Select a fighter --" if x == '' else x
            )
            
            if selected and selected != '':
                fighter = fighters_df[fighters_df['Full Name'] == selected].iloc[0]
                
                st.markdown(f"### 🥊 {fighter['First Name']} {fighter['Last Name']}")
                if fighter['Nickname']:
                    st.markdown(f"**Nickname:** *'{fighter['Nickname']}'*")
                
                st.markdown("---")
                fighter_card(fighter)
            else:
                st.info("👆 Select a fighter from the dropdown")
    
    # Show top fighters if no search
    if (search_method == "🔍 Smart Search" and not query) or (search_method == "📋 Dropdown" and not selected):
        st.markdown("---")
        st.markdown("### 🏆 Top 10 Fighters by Wins")
        top_fighters = fighters_df.nlargest(10, 'Wins')[
            ['First Name', 'Last Name', 'Nickname', 'Wins', 'Losses', 'Draws', 'Weight', 'Win Rate']
        ]
        st.dataframe(top_fighters, use_container_width=True, hide_index=True)
