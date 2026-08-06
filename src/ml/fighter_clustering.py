"""
Fighter Clustering — K-Means + PCA
Groups all UFC fighters into 4 archetypes based on performance stats.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.config.settings import FIGHTERS_CSV

try:
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

ARCHETYPE_NAMES = {
    0: ("🔴 Finisher", "#e74c3c"),
    1: ("🔵 Decision Machine", "#3498db"),
    2: ("🟢 Rising Star", "#2ecc71"),
    3: ("⚪ Veteran", "#95a5a6"),
}

ARCHETYPE_DESC = {
    "🔴 Finisher": "High win rate, tends to finish fights early. Dominant and explosive.",
    "🔵 Decision Machine": "Goes the distance. High volume, technically sound, wins on points.",
    "🟢 Rising Star": "Fewer fights but impressive win rate. Future top contender.",
    "⚪ Veteran": "Battle-tested with many fights. Experienced across all situations.",
}


def load_and_cluster():
    """
    Load fighter data, engineer features, run K-Means + PCA.
    Returns enriched DataFrame with 'Cluster', 'Archetype', 'PCA_X', 'PCA_Y'.
    """
    if not SKLEARN_AVAILABLE:
        return None

    fighters = pd.read_csv(FIGHTERS_CSV)
    fighters['Full Name'] = (
        fighters['First Name'].fillna('') + ' ' + fighters['Last Name'].fillna('')
    ).str.strip()
    fighters['Total Fights'] = fighters['Wins'] + fighters['Losses'] + fighters['Draws']
    fighters['Win Rate'] = (
        fighters['Wins'] / fighters['Total Fights'].replace(0, np.nan) * 100
    ).fillna(0).round(2)
    fighters['Loss Rate'] = (
        fighters['Losses'] / fighters['Total Fights'].replace(0, np.nan) * 100
    ).fillna(0).round(2)

    # Encode stance
    stance_map = {'Orthodox': 0, 'Southpaw': 1, 'Switch': 2, 'Open Stance': 3, 'Sideways': 4}
    fighters['Stance_Enc'] = fighters['Stance'].map(stance_map).fillna(0)

    feature_cols = ['Wins', 'Losses', 'Total Fights', 'Win Rate', 'Loss Rate', 'Stance_Enc']
    df_clean = fighters.dropna(subset=['Wins', 'Losses', 'Total Fights']).copy()

    X = df_clean[feature_cols].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=20)
    df_clean['Cluster'] = kmeans.fit_predict(X_scaled)

    # Assign archetype labels based on cluster centers
    centers = kmeans.cluster_centers_
    # win_rate is index 3 in feature_cols, total_fights is index 2
    win_rate_rank = centers[:, 3].argsort()[::-1]   # highest win rate first
    total_fight_rank = centers[:, 2].argsort()[::-1]  # most fights first

    # Heuristic labeling:
    # Finisher = highest win rate with moderate fights
    # Rising Star = highest win rate with few fights
    # Veteran = most total fights
    # Decision Machine = rest

    cluster_stats = []
    for i in range(4):
        mask = df_clean['Cluster'] == i
        avg_wr = df_clean.loc[mask, 'Win Rate'].mean()
        avg_tf = df_clean.loc[mask, 'Total Fights'].mean()
        cluster_stats.append((i, avg_wr, avg_tf))

    sorted_by_wr = sorted(cluster_stats, key=lambda x: x[1], reverse=True)
    sorted_by_tf = sorted(cluster_stats, key=lambda x: x[2], reverse=True)

    archetype_map = {}
    veteran_id = sorted_by_tf[0][0]
    archetype_map[veteran_id] = 3  # Veteran = most fights

    remaining = [c for c in cluster_stats if c[0] != veteran_id]
    remaining_by_wr = sorted(remaining, key=lambda x: x[1], reverse=True)

    high_wr_clusters = remaining_by_wr[:2]
    # Rising Star = high WR but fewer fights
    rising_star_id = min(high_wr_clusters, key=lambda x: x[2])[0]
    finisher_id = max(high_wr_clusters, key=lambda x: x[2])[0]
    archetype_map[rising_star_id] = 2  # Rising Star
    archetype_map[finisher_id] = 0    # Finisher

    leftover = [c for c in remaining if c[0] not in archetype_map]
    if leftover:
        archetype_map[leftover[0][0]] = 1  # Decision Machine

    df_clean['Archetype_ID'] = df_clean['Cluster'].map(archetype_map)
    df_clean['Archetype'] = df_clean['Archetype_ID'].map(
        lambda x: ARCHETYPE_NAMES.get(x, ("Unknown", "#aaa"))[0]
    )
    df_clean['Archetype_Color'] = df_clean['Archetype_ID'].map(
        lambda x: ARCHETYPE_NAMES.get(x, ("Unknown", "#aaa"))[1]
    )

    # PCA for 2D visualization
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    df_clean['PCA_X'] = coords[:, 0]
    df_clean['PCA_Y'] = coords[:, 1]

    return df_clean


def get_archetype_for_fighter(df_clustered, full_name: str) -> str:
    """Return the archetype label for a given fighter."""
    row = df_clustered[df_clustered['Full Name'] == full_name]
    if len(row) == 0:
        return "Unknown"
    return row.iloc[0]['Archetype']
