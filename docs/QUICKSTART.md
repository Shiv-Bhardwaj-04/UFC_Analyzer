# 🚀 Quick Start Guide

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage

### Fighter Search

**Method 1: Smart Search**
1. Go to "🔍 Fighter Search" page
2. Select "🔍 Smart Search"
3. Type any part of fighter's name:
   - First name: "Max"
   - Last name: "Holloway"
   - Nickname: "Blessed"
   - Full name: "Max Holloway"

**Method 2: Dropdown**
1. Go to "🔍 Fighter Search" page
2. Select "📋 Dropdown"
3. Choose from the complete list of fighters

### Event Analysis
1. Navigate to "📅 Events"
2. Select an event from the dropdown
3. View fight statistics and outcomes

### Fighter Comparison
1. Go to "⚔️ Compare"
2. Select two fighters from dropdowns
3. Click "Compare Fighters"
4. View side-by-side comparison

### Rankings
1. Navigate to "🏆 Rankings"
2. Choose from three tabs:
   - 🥇 Most Wins
   - 📈 Best Win Rate
   - 🔥 Most Active

## 🔍 Search Examples

| Query | Result |
|-------|--------|
| "Holloway" | Max Holloway |
| "Blessed" | Max Holloway (by nickname) |
| "Cerrone" | Donald Cerrone |
| "Cowboy" | Donald Cerrone (by nickname) |
| "Jon Jones" | Jon Jones |
| "Holoway" | Max Holloway (handles typo) |

## 💡 Tips

- **Typo Tolerance**: The search handles spelling mistakes
- **Partial Matching**: Type any part of the name
- **Suggestions**: Get suggestions if no exact match
- **Autocomplete**: Use dropdown for browsing
- **Hover Charts**: Hover over charts for detailed info

## 🐛 Troubleshooting

### Application won't start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Data not loading
- Ensure CSV files are in `src/data/` directory
- Check file permissions

### Search not working
- Try using the dropdown method
- Check spelling
- Use partial names

## 📞 Support

For issues or questions, refer to:
- `README.md` - Full documentation
- `docs/ARCHITECTURE.md` - Technical details
