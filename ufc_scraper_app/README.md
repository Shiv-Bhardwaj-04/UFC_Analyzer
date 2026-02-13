# UFC Fight Predictor & Analytics

A complete ML-powered Streamlit web application to scrape, analyze, and predict UFC fight outcomes with intelligent Q&A capabilities.

## 📁 Project Structure

```
ufc_scraper_app/
├── scrapers/              # Data scraping modules
│   ├── fighter_scraper.py # Fighter data scraper
│   ├── event_scraper.py   # Event data scraper
│   └── __init__.py
├── ml_models/             # Machine learning models
│   ├── fight_predictor.py # Fight outcome predictor
│   ├── question_answering.py # Intelligent Q&A system
│   └── __init__.py
├── data/                  # Generated CSV files & trained models
│   ├── ufc_fighters.csv
│   ├── ufc_event_data.csv
│   └── ufc_model.pkl
├── assets/                # UI assets
│   └── style.css         # Custom UFC-themed styling
├── .streamlit/           # Streamlit configuration
│   └── config.toml
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md
```

## 🚀 Setup & Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser at `http://localhost:8501`

## 🌐 Deploy to Cloud

For cloud hosting (Streamlit Cloud, AWS, etc.), set the entrypoint to `app.py`.

## 📊 Features

### 1. Data Scraper
- **Fighter Scraper**: Scrapes all UFC fighters with complete stats
- **Event Scraper**: Scrapes all UFC events with detailed fight data
- Real-time data preview and CSV export

### 2. ML Model Training
- Trains Gradient Boosting Classifier on historical fight data
- Feature engineering: height/reach/weight differences, win rates, experience
- Model evaluation with accuracy metrics and classification reports
- Saves trained model for predictions

### 3. Fight Predictor
- Select any two fighters from the database
- ML-powered fight outcome prediction
- Win probability for each fighter
- Confidence scores and visual probability bars

### 4. Intelligent Q&A System
- Ask natural language questions about UFC data
- Context-aware: detects out-of-context questions
- Answers questions like:
  - "Who has the most wins?"
  - "What is Conor McGregor's record?"
  - "Compare Jon Jones vs Daniel Cormier"
  - "Who has the longest reach?"
  - "What are the most common weight classes?"
  - "List top 10 fighters by wins"

### 5. Beautiful UFC-Themed UI
- Custom CSS with UFC octagon-inspired design
- Dark theme with red accents
- Background images and smooth animations
- Responsive layout for all devices

## 🤖 ML Model Details

**Algorithm**: Gradient Boosting Classifier
**Features**:
- Physical attributes (height, reach, weight)
- Fighter statistics (wins, losses, win rate)
- Experience level (total fights)
- Comparative features (differences between fighters)
- Weight class and stance encoding

**Performance**: ~65-70% accuracy on historical UFC data

## 💬 Valid Questions for Q&A

The system can answer:
- Fighter records and statistics
- Fighter comparisons
- Top performers by various metrics
- Event and fight statistics
- Weight class information
- Physical attributes (height, reach, weight)

**Out-of-context detection**: Automatically rejects non-UFC related questions

## 🎨 UI Customization

Edit `assets/style.css` to customize:
- Color scheme
- Background images
- Button styles
- Card layouts
- Animations
