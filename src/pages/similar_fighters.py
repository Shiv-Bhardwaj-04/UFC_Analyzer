"""
Similar Fighters Page — KNN-based fighter similarity search
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render(fighters_df, similarity_engine):
    st.markdown("""
    <div class='page-hero'>
        <h1 class='page-title'>🔗 SIMILAR FIGHTERS</h1>
        <p class='page-subtitle'>KNN algorithm finds the 5 most statistically similar fighters to any fighter</p>
    </div>
    """, unsafe_allow_html=True)

    if not similarity_engine.sklearn_available:
        st.error("⚠️ scikit-learn not installed.")
        return

    if not similarity_engine.trained:
        with st.spinner("🧠 Building KNN similarity index..."):
            similarity_engine.train(fighters_df)

    st.markdown("""
    <div class='info-box'>
        <p>🔗 <strong>How it works:</strong> Uses K-Nearest Neighbors (KNN) on normalized fighter stats
        (Wins, Losses, Win Rate, Total Fights, Stance) to find fighters with the most similar career profiles.</p>
    </div>
    """, unsafe_allow_html=True)

    fighter_names = sorted(fighters_df['Full Name'].tolist())
    selected = st.selectbox(
        "🔍 Select a fighter to find similar fighters",
        fighter_names,
        index=fighter_names.index("Donald Cerrone") if "Donald Cerrone" in fighter_names else 0
    )

    n_results = st.slider("Number of similar fighters to show", min_value=3, max_value=10, value=5)

    if st.button("🔗 Find Similar Fighters", type="primary", use_container_width=True):
        with st.spinner(f"Finding fighters similar to {selected}..."):
            similar_df = similarity_engine.find_similar(selected, n=n_results)

        if similar_df.empty:
            st.warning(f"No similar fighters found for '{selected}'.")
            return

        # Selected fighter profile
        base = fighters_df[fighters_df['Full Name'] == selected].iloc[0]
        total = base['Wins'] + base['Losses'] + base['Draws']
        base_wr = round(base['Wins'] / total * 100, 1) if total > 0 else 0

        st.markdown("---")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("#### 🥊 Selected Fighter")
            st.markdown(f"""
            <div style='background: #d6272815; border: 2px solid #d62728;
                        border-radius: 12px; padding: 1.5rem;'>
                <div style='font-size: 1.3rem; font-weight: 800; color: #d62728;'>{selected}</div>
                <div style='color: #aaa; margin-top: 0.5rem;'>
                    <b>Nickname:</b> {base.get('Nickname', '—') if str(base.get('Nickname','nan')) != 'nan' else '—'}<br>
                    <b>Record:</b> {int(base['Wins'])}W - {int(base['Losses'])}L - {int(base['Draws'])}D<br>
                    <b>Win Rate:</b> <span style='color:#2ecc71'>{base_wr}%</span><br>
                    <b>Weight:</b> {base.get('Weight','—')}<br>
                    <b>Stance:</b> {base.get('Stance','—') if str(base.get('Stance','nan')) != 'nan' else '—'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🔗 Most Similar Fighters")
            for _, row in similar_df.iterrows():
                sim_pct = row['Similarity']
                bar_color = "#2ecc71" if sim_pct >= 70 else "#f39c12" if sim_pct >= 50 else "#e74c3c"
                st.markdown(f"""
                <div style='background: #111; border: 1px solid #333; border-radius: 10px;
                            padding: 1rem; margin-bottom: 0.6rem;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-weight: 700; color: #fff; font-size: 1rem;'>{row['Fighter']}</span>
                        <span style='color: {bar_color}; font-weight: 700;'>{sim_pct:.0f}% match</span>
                    </div>
                    <div style='background: #222; border-radius: 6px; height: 6px; margin: 0.5rem 0;'>
                        <div style='background: {bar_color}; width: {sim_pct}%; height: 6px; border-radius: 6px;'></div>
                    </div>
                    <div style='color: #888; font-size: 0.82rem;'>
                        {row['Wins']}W - {row['Losses']}L &nbsp;|&nbsp;
                        Win Rate: <b style='color:#ccc'>{row['Win Rate']}</b> &nbsp;|&nbsp;
                        {row['Weight']} &nbsp;|&nbsp; {row['Stance']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Comparison radar/bar chart
        st.markdown("---")
        st.markdown("### 📊 Stats Comparison")

        compare_names = [selected] + similar_df['Fighter'].tolist()
        compare_df_list = []
        for name in compare_names:
            row = fighters_df[fighters_df['Full Name'] == name]
            if len(row) == 0:
                continue
            r = row.iloc[0]
            tot = r['Wins'] + r['Losses'] + r['Draws']
            wr = round(r['Wins'] / tot * 100, 1) if tot > 0 else 0
            compare_df_list.append({
                'Fighter': name,
                'Wins': int(r['Wins']),
                'Losses': int(r['Losses']),
                'Total Fights': int(tot),
                'Win Rate (%)': wr
            })

        compare_df = pd.DataFrame(compare_df_list)

        fig = go.Figure()
        colors = ['#d62728'] + ['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#e74c3c', '#95a5a6', '#34495e', '#16a085']
        for i, (_, row) in enumerate(compare_df.iterrows()):
            is_base = row['Fighter'] == selected
            fig.add_trace(go.Bar(
                name=row['Fighter'],
                x=['Wins', 'Losses', 'Total Fights', 'Win Rate (%)'],
                y=[row['Wins'], row['Losses'], row['Total Fights'], row['Win Rate (%)']],
                marker_color=colors[i % len(colors)],
                opacity=1.0 if is_base else 0.75,
            ))

        fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#0d0d1a',
            font_color='#ccc',
            height=380,
            xaxis=dict(gridcolor='#1e1e2e'),
            yaxis=dict(gridcolor='#1e1e2e'),
            legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='#333'),
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Table
        st.dataframe(compare_df, use_container_width=True, hide_index=True)

        with st.expander("🔬 How KNN similarity works"):
            st.markdown("""
            **Algorithm**: K-Nearest Neighbors (KNN) with Euclidean distance

            **Feature vector** (per fighter, StandardScaler normalized):
            - Wins, Losses, Total Fights, Win Rate (%), Stance (encoded)

            **Similarity %** is computed as: `max(0, 100 − distance × 10)`

            Higher % = more similar career profile. 100% = identical stats.

            KNN does **no training** — it memorizes all fighters and finds
            the closest points in 5D feature space at query time.
            """)
