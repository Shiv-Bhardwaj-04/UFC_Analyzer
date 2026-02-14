"""
Home Dashboard Page
"""
import streamlit as st
import plotly.express as px
from src.components.ui_components import page_header, metric_card


def render(fighters_df, events_df):
    """Render home dashboard"""
    page_header("🥊 UFC ANALYTICS DASHBOARD", "Comprehensive UFC Fighter & Event Statistics")
    
    # Welcome message
    st.markdown("""
    <div class='info-box'>
        <h3>👋 Welcome to UFC Analytics!</h3>
        <p>Professional MMA statistics platform providing in-depth analysis of UFC fighters, events, and performance metrics.</p>
        <p><strong>Select a page from the sidebar to get started!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("### 📊 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(f"{len(fighters_df):,}", "🥊 Total Fighters", 'purple')
    
    with col2:
        metric_card(f"{events_df['Event Name'].nunique():,}", "📅 Total Events", 'pink')
    
    with col3:
        metric_card(f"{len(events_df):,}", "🥊 Total Fights", 'blue')
    
    with col4:
        avg_wins = fighters_df['Wins'].mean()
        metric_card(f"{avg_wins:.1f}", "🏆 Avg Wins/Fighter", 'green')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Top 10 Weight Classes")
        weight_counts = fighters_df['Weight'].value_counts().head(10)
        fig = px.bar(
            x=weight_counts.index, 
            y=weight_counts.values,
            labels={'x': 'Weight Class', 'y': 'Number of Fighters'},
            color=weight_counts.values,
            color_continuous_scale='Reds',
            text=weight_counts.values
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🥋 Fighting Stance Distribution")
        stance_counts = fighters_df['Stance'].value_counts()
        fig = px.pie(
            values=stance_counts.values,
            names=stance_counts.index,
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Win/Loss Analysis
    st.markdown("### 📈 Fighter Performance Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Wins Distribution**")
        fig = px.histogram(
            fighters_df, 
            x='Wins', 
            nbins=30,
            labels={'Wins': 'Number of Wins', 'count': 'Number of Fighters'},
            color_discrete_sequence=['#2ecc71']
        )
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Losses Distribution**")
        fig = px.histogram(
            fighters_df,
            x='Losses',
            nbins=30,
            labels={'Losses': 'Number of Losses', 'count': 'Number of Fighters'},
            color_discrete_sequence=['#e74c3c']
        )
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
