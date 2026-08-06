"""
Fighter DNA Page — K-Means Clustering with PCA visualization
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.ml.fighter_clustering import ARCHETYPE_DESC


def render(fighters_df, clustered_df):
    st.markdown("""
    <div class='page-hero'>
        <h1 class='page-title'>🧬 FIGHTER DNA</h1>
        <p class='page-subtitle'>K-Means clustering reveals 4 hidden fighter archetypes across 1,941 fighters</p>
    </div>
    """, unsafe_allow_html=True)

    if clustered_df is None:
        st.error("⚠️ Clustering unavailable. Install scikit-learn: `pip install scikit-learn`")
        return

    # Archetype cards
    archetypes = clustered_df.groupby('Archetype')
    archetype_list = sorted(clustered_df['Archetype'].unique())

    cols = st.columns(len(archetype_list))
    for col, arch in zip(cols, archetype_list):
        color = clustered_df[clustered_df['Archetype'] == arch]['Archetype_Color'].iloc[0]
        count = len(clustered_df[clustered_df['Archetype'] == arch])
        avg_wr = clustered_df[clustered_df['Archetype'] == arch]['Win Rate'].mean()
        avg_tf = clustered_df[clustered_df['Archetype'] == arch]['Total Fights'].mean()
        desc = ARCHETYPE_DESC.get(arch, "")
        with col:
            st.markdown(f"""
            <div style='background: {color}18; border: 1.5px solid {color}55;
                        border-radius: 12px; padding: 1.2rem; text-align: center;
                        min-height: 160px;'>
                <div style='font-size: 1.3rem; font-weight: 700; color: {color};'>{arch}</div>
                <div style='font-size: 1.8rem; font-weight: 900; color: #fff; margin: 0.3rem 0;'>{count}</div>
                <div style='font-size: 0.75rem; color: #aaa;'>fighters</div>
                <div style='font-size: 0.8rem; color: #ccc; margin-top: 0.5rem;'>
                    Avg WR: <b style='color:{color}'>{avg_wr:.1f}%</b> &nbsp;|&nbsp;
                    Avg Fights: <b>{avg_tf:.0f}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        weight_options = ['All Weight Classes'] + sorted(clustered_df['Weight'].dropna().unique().tolist())
        selected_weight = st.selectbox("Filter by Weight Class", weight_options)
    with col2:
        show_labels = st.checkbox("Show fighter names on chart", value=False)

    df_plot = clustered_df.copy()
    if selected_weight != 'All Weight Classes':
        df_plot = df_plot[df_plot['Weight'] == selected_weight]

    # PCA scatter plot
    st.markdown("### 🗺️ Fighter DNA Map (PCA)")
    st.caption("Each dot = one fighter. Position reflects fighting stats. Hover for details.")

    hover_data = {
        'Full Name': True, 'Archetype': True,
        'Wins': True, 'Losses': True, 'Win Rate': True,
        'Total Fights': True, 'PCA_X': False, 'PCA_Y': False
    }

    color_map = {}
    for _, row in df_plot.iterrows():
        color_map[row['Archetype']] = row['Archetype_Color']

    fig = px.scatter(
        df_plot, x='PCA_X', y='PCA_Y',
        color='Archetype',
        color_discrete_map=color_map,
        hover_data=hover_data,
        text='Full Name' if show_labels else None,
        size_max=12,
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=7))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#0d0d1a',
        font_color='#ccc',
        height=520,
        xaxis=dict(title="PCA Component 1", gridcolor='#1e1e2e', zerolinecolor='#333'),
        yaxis=dict(title="PCA Component 2", gridcolor='#1e1e2e', zerolinecolor='#333'),
        legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='#333', borderwidth=1),
        margin=dict(t=20, b=20)
    )
    if show_labels:
        fig.update_traces(textposition='top center', textfont=dict(size=8, color='#aaa'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Archetype deep dives
    st.markdown("### 📋 Archetype Breakdown")
    tabs = st.tabs(archetype_list)
    for tab, arch in zip(tabs, archetype_list):
        with tab:
            arch_df = clustered_df[clustered_df['Archetype'] == arch]
            color = arch_df['Archetype_Color'].iloc[0]
            desc = ARCHETYPE_DESC.get(arch, "")
            st.markdown(f"<p style='color:{color}; font-style:italic;'>{desc}</p>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Top 15 fighters in this archetype:**")
                top15 = arch_df.nlargest(15, 'Wins')[
                    ['Full Name', 'Weight', 'Wins', 'Losses', 'Win Rate', 'Total Fights']
                ].copy()
                top15['Win Rate'] = top15['Win Rate'].apply(lambda x: f"{x:.1f}%")
                st.dataframe(top15, use_container_width=True, hide_index=True)
            with col2:
                st.markdown("**Stats distribution:**")
                fig2 = px.histogram(
                    arch_df, x='Win Rate', nbins=20,
                    color_discrete_sequence=[color],
                    labels={'Win Rate': 'Win Rate (%)', 'count': 'Fighters'}
                )
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0d0d1a',
                    font_color='#ccc', height=280,
                    xaxis=dict(gridcolor='#1e1e2e'), yaxis=dict(gridcolor='#1e1e2e'),
                    margin=dict(t=10, b=10)
                )
                st.plotly_chart(fig2, use_container_width=True)

    # Lookup your fighter's archetype
    st.markdown("---")
    st.markdown("### 🔍 Find Your Fighter's Archetype")
    fighter_names = sorted(clustered_df['Full Name'].tolist())
    selected = st.selectbox("Select a fighter", fighter_names, key="dna_lookup")
    if selected:
        row = clustered_df[clustered_df['Full Name'] == selected].iloc[0]
        color = row['Archetype_Color']
        st.markdown(f"""
        <div style='background: {color}18; border: 2px solid {color};
                    border-radius: 12px; padding: 1.5rem; margin-top: 1rem;'>
            <span style='font-size: 1.5rem; font-weight: 800; color:{color};'>{row['Archetype']}</span>
            <p style='color:#ccc; margin-top: 0.5rem;'>{ARCHETYPE_DESC.get(row['Archetype'], '')}</p>
            <p style='color:#aaa;'>Record: <b>{int(row['Wins'])}W - {int(row['Losses'])}L - {int(row['Draws'])}D</b> &nbsp;|&nbsp;
            Win Rate: <b style='color:{color}'>{row['Win Rate']:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
