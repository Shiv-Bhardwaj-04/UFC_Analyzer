"""
Fight Outcome Predictor — Random Forest Classifier
Trained on historical UFC fight data with balanced classes.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.config.settings import FIGHTERS_CSV, EVENTS_CSV

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score, classification_report
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


FEATURE_COLS = [
    'f1_Wins', 'f1_Losses', 'f1_Draws', 'f1_Total Fights', 'f1_Win Rate',
    'f2_Wins', 'f2_Losses', 'f2_Draws', 'f2_Total Fights', 'f2_Win Rate',
    'win_rate_diff', 'experience_diff', 'wins_diff'
]


def _parse_height_to_inches(h):
    """Convert height string like 5' 10\" to inches float."""
    try:
        if '--' in str(h) or str(h).strip() == '':
            return np.nan
        parts = str(h).replace('"', '').split("'")
        feet = int(parts[0].strip())
        inches = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 0
        return feet * 12 + inches
    except Exception:
        return np.nan


def _parse_reach(r):
    """Convert reach string like 72.0\" to float."""
    try:
        if '--' in str(r) or str(r).strip() == '':
            return np.nan
        return float(str(r).replace('"', '').strip())
    except Exception:
        return np.nan


def _load_and_preprocess():
    """Load and preprocess both datasets into a training dataframe."""
    fighters = pd.read_csv(FIGHTERS_CSV)
    events = pd.read_csv(EVENTS_CSV)

    fighters['Full Name'] = (
        fighters['First Name'].fillna('') + ' ' + fighters['Last Name'].fillna('')
    ).str.strip()
    fighters['Total Fights'] = fighters['Wins'] + fighters['Losses'] + fighters['Draws']
    fighters['Win Rate'] = (
        fighters['Wins'] / fighters['Total Fights'].replace(0, np.nan) * 100
    ).fillna(0).round(2)

    # De-duplicate fighters (keep the one with most fights)
    fighters = fighters.sort_values('Total Fights', ascending=False).drop_duplicates('Full Name')

    stats_cols = ['Full Name', 'Wins', 'Losses', 'Draws', 'Total Fights', 'Win Rate']
    fighter_stats = fighters[stats_cols].set_index('Full Name')

    # Only keep fights where both fighters are in the DB
    both = events[
        events['Fighter1'].isin(fighter_stats.index) &
        events['Fighter2'].isin(fighter_stats.index)
    ].copy()

    if len(both) == 0:
        return None, None

    # Merge fighter stats
    ml_df = both[['Fighter1', 'Fighter2', 'Weight Class']].copy()
    ml_df = ml_df.merge(
        fighter_stats.add_prefix('f1_'), left_on='Fighter1', right_index=True
    )
    ml_df = ml_df.merge(
        fighter_stats.add_prefix('f2_'), left_on='Fighter2', right_index=True
    )
    ml_df['winner'] = 1  # Fighter1 is always winner in the dataset

    # Create mirrored (balanced) dataset — swap fighters, label = 0
    ml_flip = ml_df.copy()
    rename_map = {}
    for c in ml_df.columns:
        if c.startswith('f1_'):
            rename_map[c] = c.replace('f1_', 'f2_')
        elif c.startswith('f2_'):
            rename_map[c] = c.replace('f2_', 'f1_')
    ml_flip = ml_flip.rename(columns=rename_map)
    ml_flip['winner'] = 0

    ml_full = pd.concat([ml_df, ml_flip], ignore_index=True)

    # Engineer delta features
    ml_full['win_rate_diff'] = ml_full['f1_Win Rate'] - ml_full['f2_Win Rate']
    ml_full['experience_diff'] = ml_full['f1_Total Fights'] - ml_full['f2_Total Fights']
    ml_full['wins_diff'] = ml_full['f1_Wins'] - ml_full['f2_Wins']

    ml_full = ml_full.dropna(subset=FEATURE_COLS)

    X = ml_full[FEATURE_COLS]
    y = ml_full['winner']
    return X, y


class FightPredictor:
    """Random Forest fight outcome predictor."""

    def __init__(self):
        self.model = None
        self.cv_accuracy = None
        self.trained = False
        self.sklearn_available = SKLEARN_AVAILABLE

    def train(self):
        """Train the Random Forest model."""
        if not SKLEARN_AVAILABLE:
            return False

        X, y = _load_and_preprocess()
        if X is None or len(X) < 100:
            return False

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_split=10,
            random_state=42,
            n_jobs=-1
        )
        # Cross-validated accuracy
        scores = cross_val_score(self.model, X, y, cv=5, scoring='accuracy')
        self.cv_accuracy = scores.mean()
        self.cv_std = scores.std()

        # Train on full data for prediction
        self.model.fit(X, y)
        self.feature_importances = dict(zip(FEATURE_COLS, self.model.feature_importances_))
        self.trained = True
        return True

    def predict(self, fighter1_stats: dict, fighter2_stats: dict) -> dict:
        """
        Predict fight outcome between two fighters.

        Parameters
        ----------
        fighter1_stats, fighter2_stats : dict with keys:
            Wins, Losses, Draws, Total Fights, Win Rate

        Returns
        -------
        dict with keys: winner (1 or 2), f1_probability, f2_probability
        """
        if not self.trained or not SKLEARN_AVAILABLE:
            return None

        def make_row(f1, f2):
            return {
                'f1_Wins': f1['Wins'],
                'f1_Losses': f1['Losses'],
                'f1_Draws': f1['Draws'],
                'f1_Total Fights': f1['Total Fights'],
                'f1_Win Rate': f1['Win Rate'],
                'f2_Wins': f2['Wins'],
                'f2_Losses': f2['Losses'],
                'f2_Draws': f2['Draws'],
                'f2_Total Fights': f2['Total Fights'],
                'f2_Win Rate': f2['Win Rate'],
                'win_rate_diff': f1['Win Rate'] - f2['Win Rate'],
                'experience_diff': f1['Total Fights'] - f2['Total Fights'],
                'wins_diff': f1['Wins'] - f2['Wins'],
            }

        row = make_row(fighter1_stats, fighter2_stats)
        X = pd.DataFrame([row])
        proba = self.model.predict_proba(X)[0]

        # class 0 = fighter2 wins, class 1 = fighter1 wins
        classes = list(self.model.classes_)
        f1_prob = proba[classes.index(1)] if 1 in classes else 0.5
        f2_prob = 1.0 - f1_prob

        return {
            'winner': 1 if f1_prob >= 0.5 else 2,
            'f1_probability': round(f1_prob * 100, 1),
            'f2_probability': round(f2_prob * 100, 1),
            'confidence': round(max(f1_prob, f2_prob) * 100, 1),
        }
