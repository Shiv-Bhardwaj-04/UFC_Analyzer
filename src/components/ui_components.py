"""
Reusable UI components for the dashboard
"""
import streamlit as st
import plotly.graph_objects as go
from src.config.settings import GRADIENT_COLORS, CHART_COLORS


def metric_card(value, label, gradient='purple'):
    """Display a metric card with gradient background"""
    st.markdown(f"""
    <div style='background: {GRADIENT_COLORS[gradient]}; 
                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
        <h2 style='margin: 0;'>{value}</h2>
        <p style='margin: 0;'>{label}</p>
    </div>
    """, unsafe_allow_html=True)


def info_box(title, content):
    """Display an info box"""
    st.markdown(f"""
    <div class='info-box'>
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def fighter_card(fighter):
    """Display fighter information card"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📍 Personal Info**")
        st.write(f"➡️ Height: {fighter['Height']}")
        st.write(f"➡️ Weight: {fighter['Weight']}")
        st.write(f"➡️ Reach: {fighter['Reach']}")
        st.write(f"➡️ Stance: {fighter['Stance']}")
    
    with col2:
        st.markdown("**🏆 Fight Record**")
        total_fights = fighter['Wins'] + fighter['Losses'] + fighter['Draws']
        win_rate = (fighter['Wins'] / total_fights * 100) if total_fights > 0 else 0
        st.write(f"✅ Wins: **{fighter['Wins']}**")
        st.write(f"❌ Losses: **{fighter['Losses']}**")
        st.write(f"🤝 Draws: **{fighter['Draws']}**")
        st.write(f"📈 Win Rate: **{win_rate:.1f}%**")
    
    with col3:
        st.markdown("**📉 Performance Chart**")
        fig = go.Figure(data=[
            go.Bar(name='Wins', x=['Record'], y=[fighter['Wins']], marker_color=CHART_COLORS['wins']),
            go.Bar(name='Losses', x=['Record'], y=[fighter['Losses']], marker_color=CHART_COLORS['losses']),
            go.Bar(name='Draws', x=['Record'], y=[fighter['Draws']], marker_color=CHART_COLORS['draws'])
        ])
        fig.update_layout(height=250, showlegend=True, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)


def page_header(title, subtitle):
    """Display page header"""
    st.markdown(f"<div class='main-header'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{subtitle}</div>", unsafe_allow_html=True)


def suggestion_box(suggestions):
    """Display search suggestions"""
    if not suggestions:
        return
    
    st.markdown("""
    <div class='suggestion-box'>
        <h4>💡 Did you mean?</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for suggestion in suggestions:
        st.button(f"👉 {suggestion.title()}", key=f"suggest_{suggestion}")
