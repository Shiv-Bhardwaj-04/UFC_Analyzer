"""
Configuration settings for UFC Analytics Dashboard
"""
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "src" / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Data files
FIGHTERS_CSV = DATA_DIR / "ufc_fighters.csv"
EVENTS_CSV = DATA_DIR / "ufc_event_data.csv"

# App settings
APP_TITLE = "UFC Analytics Dashboard"
APP_ICON = "🥊"
PAGE_LAYOUT = "wide"

# Search settings
FUZZY_MATCH_THRESHOLD = 0.4
MAX_SEARCH_RESULTS = 10
MIN_FIGHTS_FOR_WINRATE = 10

# Color schemes
GRADIENT_COLORS = {
    'purple': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'pink': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'blue': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'green': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
}

CHART_COLORS = {
    'wins': '#2ecc71',
    'losses': '#e74c3c',
    'draws': '#95a5a6',
    'primary': '#d62728',
}
