"""
Fight Predictor Page — ML-powered fight outcome prediction
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def render(fighters_df, predictor):
    st.markdown("""
    <div class='page-hero'>
        <h1 class='page-title'>🤖 FIGHT PREDICTOR</h1>
        <p class='page-subtitle'>Random Forest ML model trained on 2,796 historical UFC fights</p>
    </div>
    """, unsafe_allow_html=True)

    if not predictor.sklearn_available:
        st.error("⚠️ scikit-learn not installed. Run: `pip install scikit-learn`")
        return

    if not predictor.trained:
        with st.spinner("🧠 Training Random Forest model on historical fight data..."):
            success = predictor.train()
        if not success:
            st.error("❌ Model training failed. Check data files.")
            return

    # Model info banner
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='ml-stat-card'>
            <div class='ml-stat-value'>{predictor.cv_accuracy*100:.1f}%</div>
            <div class='ml-stat-label'>Model Accuracy (5-Fold CV)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='ml-stat-card'>
            <div class='ml-stat-value'>200</div>
            <div class='ml-stat-label'>Decision Trees</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='ml-stat-card'>
            <div class='ml-stat-value'>2,796</div>
            <div class='ml-stat-label'>Training Samples</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fighter selection
    st.markdown("### ⚔️ Select Your Fighters")
    fighter_names = sorted(fighters_df['Full Name'].tolist())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='fighter-select-label'>🔴 Fighter 1</div>", unsafe_allow_html=True)
        f1_name = st.selectbox("Fighter 1", fighter_names, index=fighter_names.index("Jon Jones") if "Jon Jones" in fighter_names else 0, label_visibility="collapsed", key="pred_f1")
    with col2:
        st.markdown("<div class='fighter-select-label'>🔵 Fighter 2</div>", unsafe_allow_html=True)
        f2_name = st.selectbox("Fighter 2", fighter_names, index=fighter_names.index("Max Holloway") if "Max Holloway" in fighter_names else 1, label_visibility="collapsed", key="pred_f2")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🤖 PREDICT FIGHT OUTCOME", type="primary", use_container_width=True):
        if f1_name == f2_name:
            st.warning("⚠️ Please select two different fighters.")
            return

        f1 = fighters_df[fighters_df['Full Name'] == f1_name].iloc[0]
        f2 = fighters_df[fighters_df['Full Name'] == f2_name].iloc[0]

        def to_stats(f):
            total = f['Wins'] + f['Losses'] + f['Draws']
            return {
                'Wins': int(f['Wins']),
                'Losses': int(f['Losses']),
                'Draws': int(f['Draws']),
                'Total Fights': int(total),
                'Win Rate': round(f['Wins'] / total * 100, 2) if total > 0 else 0,
            }

        result = predictor.predict(to_stats(f1), to_stats(f2))

        if result is None:
            st.error("Prediction failed.")
            return

        st.markdown("---")
        st.markdown("### 🏆 Prediction Result")

        # Winner banner
        winner_name = f1_name if result['winner'] == 1 else f2_name
        winner_prob = result['f1_probability'] if result['winner'] == 1 else result['f2_probability']
        winner_color = "#e74c3c" if result['winner'] == 1 else "#3498db"

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {winner_color}22, {winner_color}44);
                    border: 2px solid {winner_color}; border-radius: 16px;
                    padding: 2rem; text-align: center; margin: 1rem 0;'>
            <div style='font-size: 1rem; color: #aaa; margin-bottom: 0.5rem;'>PREDICTED WINNER</div>
            <div style='font-size: 2.5rem; font-weight: 900; color: {winner_color};'>{winner_name}</div>
            <div style='font-size: 1.2rem; color: #ccc; margin-top: 0.5rem;'>
                Confidence: <strong style='color:{winner_color}'>{result['confidence']}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Probability bars
        st.markdown("### 📊 Win Probability")
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['f1_probability'],
                title={'text': f"🔴 {f1_name}", 'font': {'color': '#e74c3c', 'size': 14}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#555'},
                    'bar': {'color': '#e74c3c'},
                    'bgcolor': '#1a1a2e',
                    'bordercolor': '#333',
                    'steps': [{'range': [0, 50], 'color': '#1a1a2e'}, {'range': [50, 100], 'color': '#2d1b1b'}],
                    'threshold': {'line': {'color': '#e74c3c', 'width': 3}, 'thickness': 0.75, 'value': 50}
                },
                number={'suffix': '%', 'font': {'color': '#e74c3c', 'size': 28}}
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=40, b=0, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['f2_probability'],
                title={'text': f"🔵 {f2_name}", 'font': {'color': '#3498db', 'size': 14}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#555'},
                    'bar': {'color': '#3498db'},
                    'bgcolor': '#1a1a2e',
                    'bordercolor': '#333',
                    'steps': [{'range': [0, 50], 'color': '#1a1a2e'}, {'range': [50, 100], 'color': '#1a2535'}],
                    'threshold': {'line': {'color': '#3498db', 'width': 3}, 'thickness': 0.75, 'value': 50}
                },
                number={'suffix': '%', 'font': {'color': '#3498db', 'size': 28}}
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=40, b=0, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

        # Stats comparison table
        st.markdown("### 📋 Fighter Stats Comparison")
        f1s = to_stats(f1)
        f2s = to_stats(f2)
        comp_data = {
            'Stat': ['Wins', 'Losses', 'Draws', 'Total Fights', 'Win Rate'],
            f1_name: [f1s['Wins'], f1s['Losses'], f1s['Draws'], f1s['Total Fights'], f"{f1s['Win Rate']:.1f}%"],
            f2_name: [f2s['Wins'], f2s['Losses'], f2s['Draws'], f2s['Total Fights'], f"{f2s['Win Rate']:.1f}%"],
        }
        import pandas as pd
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

        # Model transparency
        with st.expander("🔬 How does this model work?"):
            st.markdown(f"""
            **Algorithm**: Random Forest Classifier (200 decision trees)

            **Training data**: 2,796 balanced fight records from {len(fighter_names):,} UFC fighters (1994–2023)

            **Features used**:
            - Both fighters' Wins, Losses, Draws
            - Total fights (experience proxy)
            - Win Rate (%)
            - Delta features: Win Rate difference, Experience gap, Wins gap

            **Cross-validated accuracy**: **{predictor.cv_accuracy*100:.1f}%** (5-fold)

            > This accuracy is expected given we use career W/L/D stats only —
            > not fight-by-fight striking or grappling data. A model that honestly
            > predicts at ~60–65% using simple stats is **scientifically valid**.
            """)

            if hasattr(predictor, 'feature_importances'):
                fi = predictor.feature_importances
                fig = px.bar(
                    x=list(fi.values()),
                    y=list(fi.keys()),
                    orientation='h',
                    title="Feature Importances",
                    color=list(fi.values()),
                    color_continuous_scale='Reds'
                )
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  font_color='#ccc', showlegend=False, height=300)
                fig.update_xaxes(gridcolor='#333')
                fig.update_yaxes(gridcolor='#333')
                st.plotly_chart(fig, use_container_width=True)
