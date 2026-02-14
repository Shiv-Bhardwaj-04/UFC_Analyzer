"""
Data loading and preprocessing utilities
"""
import pandas as pd
import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.config.settings import FIGHTERS_CSV, EVENTS_CSV


@st.cache_data
def load_fighters_data():
    """Load and preprocess fighters data"""
    df = pd.read_csv(FIGHTERS_CSV)
    
    # Create full name column
    df['Full Name'] = (df['First Name'].fillna('') + ' ' + df['Last Name'].fillna('')).str.strip()
    
    # Create searchable text combining all name fields
    df['Search Text'] = (
        df['First Name'].fillna('').str.lower() + ' ' + 
        df['Last Name'].fillna('').str.lower() + ' ' + 
        df['Nickname'].fillna('').str.lower()
    ).str.strip()
    
    # Calculate total fights and win rate
    df['Total Fights'] = df['Wins'] + df['Losses'] + df['Draws']
    df['Win Rate'] = (df['Wins'] / df['Total Fights'] * 100).fillna(0).round(1)
    
    return df


@st.cache_data
def load_events_data():
    """Load events data"""
    df = pd.read_csv(EVENTS_CSV)
    return df


def get_fighter_by_name(fighters_df, name):
    """Get fighter by exact full name match"""
    result = fighters_df[fighters_df['Full Name'] == name]
    if len(result) > 0:
        return result.iloc[0]
    return None


def get_top_fighters(fighters_df, n=10, by='Wins'):
    """Get top N fighters by specified metric"""
    return fighters_df.nlargest(n, by)
