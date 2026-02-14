# 🥊 UFC Analytics Dashboard

Professional MMA Statistics Analysis Platform

## 📋 Overview

UFC Analytics Dashboard is a comprehensive data analysis tool for UFC statistics, providing in-depth insights into fighter performance, event analysis, and head-to-head comparisons.

## ✨ Features

### 🔍 Advanced Fighter Search
- **Multi-Strategy Search Engine**
  - Exact name matching (first name, last name, nickname)
  - Partial matching
  - Fuzzy matching (handles typos)
  - Token-based search
  - Smart suggestions

### 📊 Analytics
- Fighter performance metrics
- Weight class distribution
- Win/Loss analysis
- Event-level statistics
- Historical trends

### ⚔️ Fighter Comparison
- Side-by-side statistics
- Visual comparisons
- Record analysis
- Physical attributes comparison

### 🏆 Rankings
- Most wins
- Best win rates
- Most active fighters
- Customizable filters

## 🏗️ Project Structure

```
UFC/
├── app.py                      # Main application entry point
├── src/
│   ├── config/
│   │   └── settings.py         # Configuration settings
│   ├── data/
│   │   ├── ufc_fighters.csv    # Fighters database
│   │   └── ufc_event_data.csv  # Events database
│   ├── utils/
│   │   ├── data_loader.py      # Data loading utilities
│   │   └── search.py           # Advanced search engine
│   ├── components/
│   │   └── ui_components.py    # Reusable UI components
│   └── pages/
│       ├── home.py             # Home dashboard
│       ├── fighter_search.py   # Fighter search page
│       ├── events.py           # Events analysis
│       ├── compare.py          # Fighter comparison
│       └── rankings.py         # Rankings page
├── assets/
│   └── styles/                 # Custom styles
├── docs/                       # Documentation
├── tests/                      # Unit tests
└── requirements.txt            # Dependencies

```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
cd UFC
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## 🔍 Search Capabilities

The search engine uses multiple strategies to find fighters:

1. **Exact Match**: Direct match on first name, last name, or nickname
2. **Partial Match**: Finds fighters where query is contained in any name field
3. **Fuzzy Match**: Uses sequence matching to handle typos (threshold: 0.6)
4. **Token Match**: Matches individual words in multi-word queries
5. **Loose Match**: Very lenient fuzzy matching as fallback (threshold: 0.4)

### Search Examples
- `"Conor"` → Conor McGregor
- `"McGregor"` → Conor McGregor
- `"Notorious"` → Conor McGregor (nickname)
- `"Jon Jones"` → Jon Jones
- `"Silva"` → Multiple Silva fighters
- `"Mcgreggor"` → Conor McGregor (handles typo)

## 📊 Data

- **Fighters**: 1,941 UFC fighters
- **Events**: Historical UFC events
- **Fights**: Comprehensive fight records

## 🛠️ Technologies

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Search**: Custom multi-strategy engine with fuzzy matching

## 📖 Usage Guide

### Fighter Search
1. Navigate to "🔍 Fighter Search"
2. Choose search method:
   - **Smart Search**: Type any part of fighter's name
   - **Dropdown**: Browse all fighters
3. View detailed fighter statistics

### Event Analysis
1. Navigate to "📅 Events"
2. Select an event from dropdown
3. View fight results and statistics

### Fighter Comparison
1. Navigate to "⚔️ Compare"
2. Select two fighters
3. Click "Compare Fighters"
4. View side-by-side comparison

### Rankings
1. Navigate to "🏆 Rankings"
2. Choose ranking category:
   - Most Wins
   - Best Win Rate
   - Most Active

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is for educational purposes.

## 👨‍💻 Author

Professional MMA Statistics Platform

## 🙏 Acknowledgments

- Data source: UFC Stats
- Built with Streamlit and Plotly
