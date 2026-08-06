"""
Similar Fighters — KNN-based Fighter Similarity Search
Finds the N most similar fighters to any given fighter.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.config.settings import FIGHTERS_CSV

try:
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class FighterSimilarity:
    """KNN-based fighter similarity engine."""

    def __init__(self):
        self.model = None
        self.fighters_df = None
        self.feature_cols = ['Wins', 'Losses', 'Total Fights', 'Win Rate', 'Stance_Enc']
        self.trained = False
        self.sklearn_available = SKLEARN_AVAILABLE

    def train(self, fighters_df: pd.DataFrame = None):
        """Build KNN index on fighter stats."""
        if not SKLEARN_AVAILABLE:
            return False

        if fighters_df is None:
            fighters_df = pd.read_csv(FIGHTERS_CSV)
            fighters_df['Full Name'] = (
                fighters_df['First Name'].fillna('') + ' ' + fighters_df['Last Name'].fillna('')
            ).str.strip()

        df = fighters_df.copy()
        df['Total Fights'] = df['Wins'] + df['Losses'] + df['Draws']
        df['Win Rate'] = (
            df['Wins'] / df['Total Fights'].replace(0, np.nan) * 100
        ).fillna(0).round(2)

        stance_map = {'Orthodox': 0, 'Southpaw': 1, 'Switch': 2, 'Open Stance': 3, 'Sideways': 4}
        df['Stance_Enc'] = df['Stance'].map(stance_map).fillna(0)

        df_clean = df.dropna(subset=['Wins', 'Losses']).copy()
        X = df_clean[self.feature_cols].fillna(0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        knn = NearestNeighbors(n_neighbors=6, metric='euclidean', algorithm='auto')
        knn.fit(X_scaled)

        self.model = knn
        self.scaler = scaler
        self.fighters_df = df_clean.reset_index(drop=True)
        self.X_scaled = X_scaled
        self.trained = True
        return True

    def find_similar(self, fighter_name: str, n: int = 5) -> pd.DataFrame:
        """
        Find the n most similar fighters to the given fighter.

        Returns DataFrame with columns: Full Name, Similarity %, Wins, Losses, Win Rate
        """
        if not self.trained:
            return pd.DataFrame()

        df = self.fighters_df
        matches = df[df['Full Name'] == fighter_name]
        if len(matches) == 0:
            return pd.DataFrame()

        idx = matches.index[0]
        query = self.X_scaled[idx].reshape(1, -1)

        distances, indices = self.model.kneighbors(query, n_neighbors=n + 1)
        distances = distances[0]
        indices = indices[0]

        results = []
        for dist, i in zip(distances, indices):
            if i == idx:
                continue  # skip the fighter themselves
            row = df.iloc[i]
            # Convert distance to similarity score (0–100%)
            similarity = round(max(0, 100 - dist * 10), 1)
            results.append({
                'Fighter': row['Full Name'],
                'Similarity': similarity,
                'Weight': row.get('Weight', '—'),
                'Stance': row.get('Stance', '—'),
                'Wins': int(row['Wins']),
                'Losses': int(row['Losses']),
                'Win Rate': f"{row['Win Rate']:.1f}%",
                'Total Fights': int(row['Total Fights']),
            })

        return pd.DataFrame(results[:n])
