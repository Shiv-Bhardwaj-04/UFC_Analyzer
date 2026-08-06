"""
Fighter Comparison Page
"""
import streamlit as st
import plotly.graph_objects as go
from src.components.ui_components import page_header


def render(fighters_df):
    """Render fighter comparison page"""
    page_header("⚔️ FIGHTER COMPARISON", "Compare two fighters side-by-side")
    
    st.markdown("""
    <div class='info-box'>
        <p>⚔️ <strong>Select two fighters</strong> to compare their stats, records, and physical attributes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    fighter_names = sorted(fighters_df['Full Name'].tolist())
    
    with col1:
        fighter1_name = st.selectbox("🥊 Fighter 1", fighter_names, index=0)
    
    with col2:
        fighter2_name = st.selectbox("🥊 Fighter 2", fighter_names, index=min(1, len(fighter_names)-1))
    
    if st.button("⚔️ Compare Fighters", type="primary", use_container_width=True):
        f1 = fighters_df[fighters_df['Full Name'] == fighter1_name].iloc[0]
        f2 = fighters_df[fighters_df['Full Name'] == fighter2_name].iloc[0]
        
        st.markdown("---")
        st.markdown("### 🥊 Fighter Profiles")
        
        col1, col2, col3 = st.columns([1, 0.2, 1])
        
        with col1:
            st.markdown(f"#### 🔴 {fighter1_name}")
            st.write(f"**Nickname:** '{f1['Nickname']}'")
            st.write(f"**Record:** {f1['Wins']}-{f1['Losses']}-{f1['Draws']}")
            st.write(f"**Height:** {f1['Height']}")
            st.write(f"**Weight:** {f1['Weight']}")
            st.write(f"**Reach:** {f1['Reach']}")
            st.write(f"**Stance:** {f1['Stance']}")
            st.write(f"**Win Rate:** {f1['Win Rate']:.1f}%")
        
        with col2:
            st.markdown("<h1 style='text-align: center; color: #d62728; font-size: 4rem;'>VS</h1>", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"#### 🔵 {fighter2_name}")
            st.write(f"**Nickname:** '{f2['Nickname']}'")
            st.write(f"**Record:** {f2['Wins']}-{f2['Losses']}-{f2['Draws']}")
            st.write(f"**Height:** {f2['Height']}")
            st.write(f"**Weight:** {f2['Weight']}")
            st.write(f"**Reach:** {f2['Reach']}")
            st.write(f"**Stance:** {f2['Stance']}")
            st.write(f"**Win Rate:** {f2['Win Rate']:.1f}%")
        
        # Comparison chart
        st.markdown("### 📈 Statistical Comparison")
        
        categories = ['Wins', 'Losses', 'Draws']
        fig = go.Figure(data=[
            go.Bar(name=fighter1_name, x=categories, y=[f1['Wins'], f1['Losses'], f1['Draws']], marker_color='#e74c3c'),
            go.Bar(name=fighter2_name, x=categories, y=[f2['Wins'], f2['Losses'], f2['Draws']], marker_color='#3498db')
        ])
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
