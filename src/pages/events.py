"""
Events Analysis Page
"""
import streamlit as st
import plotly.express as px
from src.components.ui_components import page_header, metric_card


def render(events_df):
    """Render events analysis page"""
    page_header("📅 EVENT ANALYSIS", "Explore UFC events and fight statistics")
    
    st.markdown("""
    <div class='info-box'>
        <p>📅 <strong>Select an event</strong> to view detailed fight statistics and outcomes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    events = sorted(events_df['Event Name'].unique(), reverse=True)
    selected_event = st.selectbox("🎯 Select Event", events, label_visibility="collapsed")
    
    event_data = events_df[events_df['Event Name'] == selected_event]
    
    st.markdown("### 📊 Event Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric_card(f"{len(event_data)}", "🥊 Total Fights", 'purple')
    
    with col2:
        metric_card(f"{event_data['Event Date'].iloc[0]}", "📅 Event Date", 'pink')
    
    with col3:
        knockdowns = event_data['KD'].str.split('-', expand=True).astype(float).sum().sum()
        metric_card(f"{int(knockdowns)}", "💥 Total Knockdowns", 'blue')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fight results
    st.markdown("### 🥊 Fight Results")
    st.dataframe(
        event_data[['Fighter1', 'Fighter2', 'Result', 'Weight Class', 'Method', 'Round', 'Time']], 
        use_container_width=True,
        hide_index=True
    )
    
    # Statistics
    st.markdown("### 📈 Fight Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Finish Methods**")
        methods = event_data['Method'].value_counts()
        fig = px.pie(values=methods.values, names=methods.index, hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Weight Class Distribution**")
        weight_class = event_data['Weight Class'].value_counts()
        fig = px.bar(x=weight_class.index, y=weight_class.values, color=weight_class.values, color_continuous_scale='Reds')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
