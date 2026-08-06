"""
Home Dashboard — Premium Dark Theme with animated stats
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render(fighters_df, events_df):
    # Hero Section
    total_fighters = len(fighters_df)
    total_events = events_df['Event Name'].nunique()
    total_fights = len(events_df)
    avg_wins = fighters_df['Wins'].mean()

    st.markdown(f"""
    <div style='text-align: center; padding: 3rem 1rem 2rem;'>
        <div style='display: inline-block; background: linear-gradient(135deg, #d62728, #ff6b6b);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text; font-size: 3.5rem; font-weight: 900;
                    letter-spacing: -1px; line-height: 1.1;'>
            UFC ANALYTICS
        </div>
        <div style='font-size: 3.5rem; font-weight: 900; color: #fff; line-height: 1.1;'>DASHBOARD</div>
        <p style='color: #888; font-size: 1.1rem; margin-top: 1rem; max-width: 600px; margin-left: auto; margin-right: auto;'>
            Professional MMA statistics platform with ML-powered fight predictions,
            fighter DNA clustering, and deep performance analytics.
        </p>
        <div style='display: flex; gap: 0.75rem; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap;'>
            <span style='background: #d6272820; border: 1px solid #d62728; color: #d62728;
                         padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>
                🤖 ML Fight Predictor
            </span>
            <span style='background: #2ecc7120; border: 1px solid #2ecc71; color: #2ecc71;
                         padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>
                🧬 Fighter DNA
            </span>
            <span style='background: #3498db20; border: 1px solid #3498db; color: #3498db;
                         padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>
                🔗 Similarity Search
            </span>
            <span style='background: #f39c1220; border: 1px solid #f39c12; color: #f39c12;
                         padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>
                📊 Advanced EDA
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key stats
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        (col1, f"{total_fighters:,}", "Total Fighters", "#d62728"),
        (col2, f"{total_events:,}", "UFC Events", "#3498db"),
        (col3, f"{total_fights:,}", "Historical Fights", "#2ecc71"),
        (col4, f"{avg_wins:.1f}", "Avg Wins / Fighter", "#f39c12"),
    ]
    for col, val, label, color in stats:
        with col:
            st.markdown(f"""
            <div style='background: {color}12; border: 1.5px solid {color}40;
                        border-radius: 14px; padding: 1.5rem; text-align: center;'>
                <div style='font-size: 2.2rem; font-weight: 900; color: {color};'>{val}</div>
                <div style='color: #888; font-size: 0.85rem; margin-top: 0.3rem;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Charts row 1
    st.markdown("### 📊 Fighter Analytics")
    col1, col2 = st.columns(2)

    with col1:
        weight_counts = fighters_df['Weight'].value_counts().head(10)
        fig = px.bar(
            x=weight_counts.values, y=weight_counts.index,
            orientation='h',
            labels={'x': 'Fighters', 'y': 'Weight Class'},
            color=weight_counts.values,
            color_continuous_scale='Reds',
            text=weight_counts.values
        )
        fig.update_traces(textposition='outside', textfont_color='#aaa')
        fig.update_layout(
            title='Top 10 Weight Classes',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0d0d1a',
            font_color='#ccc', showlegend=False, height=380,
            xaxis=dict(gridcolor='#1e1e2e'),
            yaxis=dict(gridcolor='#1e1e2e', categoryorder='total ascending'),
            margin=dict(t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        stance_counts = fighters_df['Stance'].value_counts()
        fig = px.pie(
            values=stance_counts.values,
            names=stance_counts.index,
            color_discrete_sequence=['#d62728', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'],
            hole=0.5,
            title='Fighting Stance Distribution'
        )
        fig.update_traces(textposition='outside', textinfo='percent+label',
                          textfont_color='#ccc')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font_color='#ccc', height=380,
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Charts row 2
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(
            fighters_df, x='Wins', nbins=35,
            labels={'Wins': 'Career Wins', 'count': 'Fighters'},
            color_discrete_sequence=['#d62728'],
            title='Win Distribution Across All Fighters'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0d0d1a',
            font_color='#ccc', height=320, showlegend=False,
            xaxis=dict(gridcolor='#1e1e2e'),
            yaxis=dict(gridcolor='#1e1e2e'),
            margin=dict(t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        method_top = events_df['Method'].value_counts().head(8)
        method_labels = [m.replace('KO/TKO-', 'KO: ').replace('SUB-', 'Sub: ')
                         .replace('U-DEC', 'Unanimous Dec').replace('S-DEC', 'Split Dec')
                         .replace('M-DEC', 'Majority Dec') for m in method_top.index]
        fig = px.bar(
            x=method_top.values, y=method_labels,
            orientation='h',
            color=method_top.values,
            color_continuous_scale='Blues',
            labels={'x': 'Fights', 'y': 'Method'},
            title='Top Finish Methods (All Events)'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0d0d1a',
            font_color='#ccc', showlegend=False, height=320,
            xaxis=dict(gridcolor='#1e1e2e'),
            yaxis=dict(gridcolor='#1e1e2e', categoryorder='total ascending'),
            margin=dict(t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Platform highlights
    st.markdown("---")
    st.markdown("### 🚀 Platform Highlights")
    col1, col2, col3 = st.columns(3)
    highlights = [
        (col1, "🤖", "Fight Predictor", "#d62728",
         "Random Forest ML model trained on 2,796 historical fights. Predicts winner + confidence score."),
        (col2, "🧬", "Fighter DNA", "#2ecc71",
         "K-Means clustering segments all 1,941 fighters into 4 archetypes with PCA visualization."),
        (col3, "🔗", "Similarity Search", "#3498db",
         "KNN algorithm finds fighters with the most similar career profiles in 5D feature space."),
    ]
    for col, icon, title, color, desc in highlights:
        with col:
            st.markdown(f"""
            <div style='background: {color}10; border: 1px solid {color}33;
                        border-radius: 14px; padding: 1.5rem; height: 180px;'>
                <div style='font-size: 2rem;'>{icon}</div>
                <div style='font-weight: 700; color: {color}; font-size: 1rem; margin: 0.5rem 0;'>{title}</div>
                <div style='color: #888; font-size: 0.83rem; line-height: 1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
