import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


class UFCFightPredictor:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False
        
    def prepare_data(self, events_df, fighters_df):
        """Prepare and engineer features from raw data"""
        # Merge fighter stats with event data
        events_df = events_df.copy()
        fighters_df = fighters_df.copy()
        
        # Create full name for fighters
        fighters_df['full_name'] = fighters_df['First Name'] + ' ' + fighters_df['Last Name']
        
        # Convert height to inches
        def height_to_inches(h):
            if pd.isna(h) or h == '' or '--' in str(h):
                return 0
            try:
                parts = str(h).replace('"', '').replace("'", ' ').split()
                if len(parts) == 2:
                    return int(parts[0]) * 12 + int(parts[1])
                return 0
            except:
                return 0
        
        fighters_df['height_inches'] = fighters_df['Height'].apply(height_to_inches)
        fighters_df['reach_num'] = pd.to_numeric(fighters_df['Reach'].str.replace('"', '').str.replace('--', '0'), errors='coerce').fillna(0)
        fighters_df['weight_num'] = pd.to_numeric(fighters_df['Weight'].str.replace(' lbs.', '').str.replace('--', '0'), errors='coerce').fillna(0)
        fighters_df['wins'] = pd.to_numeric(fighters_df['Wins'], errors='coerce').fillna(0)
        fighters_df['losses'] = pd.to_numeric(fighters_df['Losses'], errors='coerce').fillna(0)
        fighters_df['draws'] = pd.to_numeric(fighters_df['Draws'], errors='coerce').fillna(0)
        fighters_df['total_fights'] = fighters_df['wins'] + fighters_df['losses'] + fighters_df['draws']
        fighters_df['win_rate'] = fighters_df.apply(
            lambda x: x['wins'] / x['total_fights'] if x['total_fights'] > 0 else 0, axis=1
        )
        
        # Merge fighter1 stats
        merged = events_df.merge(
            fighters_df[['full_name', 'height_inches', 'reach_num', 'weight_num', 'wins', 'losses', 'win_rate', 'total_fights', 'Stance']],
            left_on='Fighter1', right_on='full_name', how='left', suffixes=('', '_f1')
        )
        
        # Merge fighter2 stats
        merged = merged.merge(
            fighters_df[['full_name', 'height_inches', 'reach_num', 'weight_num', 'wins', 'losses', 'win_rate', 'total_fights', 'Stance']],
            left_on='Fighter2', right_on='full_name', how='left', suffixes=('_f1', '_f2')
        )
        
        # Create target variable (1 if Fighter1 wins, 0 otherwise)
        merged['fighter1_wins'] = (merged['Result'] == merged['Fighter1']).astype(int)
        
        # Drop draws and unknown results
        merged = merged[merged['Result'].isin([merged['Fighter1'], merged['Fighter2']])]
        
        # Feature engineering
        merged['height_diff'] = merged['height_inches_f1'] - merged['height_inches_f2']
        merged['reach_diff'] = merged['reach_num_f1'] - merged['reach_num_f2']
        merged['weight_diff'] = merged['weight_num_f1'] - merged['weight_num_f2']
        merged['win_rate_diff'] = merged['win_rate_f1'] - merged['win_rate_f2']
        merged['experience_diff'] = merged['total_fights_f1'] - merged['total_fights_f2']
        
        # Encode categorical features
        for col in ['Weight Class', 'Stance_f1', 'Stance_f2']:
            if col in merged.columns:
                le = LabelEncoder()
                merged[col + '_encoded'] = le.fit_transform(merged[col].fillna('Unknown'))
                self.label_encoders[col] = le
        
        return merged
    
    def train(self, events_csv, fighters_csv):
        """Train the prediction model"""
        events_df = pd.read_csv(events_csv)
        fighters_df = pd.read_csv(fighters_csv)
        
        data = self.prepare_data(events_df, fighters_df)
        
        self.feature_columns = [
            'height_diff', 'reach_diff', 'weight_diff', 'win_rate_diff', 
            'experience_diff', 'height_inches_f1', 'reach_num_f1', 
            'win_rate_f1', 'total_fights_f1', 'height_inches_f2', 
            'reach_num_f2', 'win_rate_f2', 'total_fights_f2',
            'Weight Class_encoded', 'Stance_f1_encoded', 'Stance_f2_encoded'
        ]
        
        X = data[self.feature_columns].fillna(0)
        y = data['fighter1_wins']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.is_trained = True
        return accuracy, classification_report(y_test, y_pred)
    
    def predict_fight(self, fighter1_stats, fighter2_stats, weight_class='Lightweight'):
        """Predict fight outcome"""
        if not self.is_trained:
            return None
        
        features = {
            'height_diff': fighter1_stats.get('height', 0) - fighter2_stats.get('height', 0),
            'reach_diff': fighter1_stats.get('reach', 0) - fighter2_stats.get('reach', 0),
            'weight_diff': fighter1_stats.get('weight', 0) - fighter2_stats.get('weight', 0),
            'win_rate_diff': fighter1_stats.get('win_rate', 0) - fighter2_stats.get('win_rate', 0),
            'experience_diff': fighter1_stats.get('total_fights', 0) - fighter2_stats.get('total_fights', 0),
            'height_inches_f1': fighter1_stats.get('height', 0),
            'reach_num_f1': fighter1_stats.get('reach', 0),
            'win_rate_f1': fighter1_stats.get('win_rate', 0),
            'total_fights_f1': fighter1_stats.get('total_fights', 0),
            'height_inches_f2': fighter2_stats.get('height', 0),
            'reach_num_f2': fighter2_stats.get('reach', 0),
            'win_rate_f2': fighter2_stats.get('win_rate', 0),
            'total_fights_f2': fighter2_stats.get('total_fights', 0),
        }
        
        # Encode categorical
        if 'Weight Class' in self.label_encoders:
            try:
                features['Weight Class_encoded'] = self.label_encoders['Weight Class'].transform([weight_class])[0]
            except:
                features['Weight Class_encoded'] = 0
        else:
            features['Weight Class_encoded'] = 0
            
        features['Stance_f1_encoded'] = 0
        features['Stance_f2_encoded'] = 0
        
        X = pd.DataFrame([features])[self.feature_columns]
        
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        return {
            'winner': 'Fighter 1' if prediction == 1 else 'Fighter 2',
            'confidence': max(probability) * 100,
            'fighter1_win_prob': probability[1] * 100,
            'fighter2_win_prob': probability[0] * 100
        }
    
    def save_model(self, path):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns,
                'is_trained': self.is_trained
            }, f)
    
    def load_model(self, path):
        """Load trained model"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.label_encoders = data['label_encoders']
            self.feature_columns = data['feature_columns']
            self.is_trained = data['is_trained']
