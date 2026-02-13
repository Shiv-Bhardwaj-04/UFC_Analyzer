# 🚀 Quick Start Guide

## Step-by-Step Instructions

### 1. Install Dependencies
Open terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### 2. Start the Application
Run the app using:
```bash
streamlit run app.py
```

Or double-click `run_app.bat` on Windows.

### 3. Use the Application

#### Step 1: Scrape Data
- Go to "📊 Data Scraper" page
- Click "Scrape Fighters" to get fighter data
- Click "Scrape Events" to get fight history
- Wait for scraping to complete (may take a few minutes)

#### Step 2: Train ML Model
- Go to "🤖 Train Model" page
- Click "🚀 Train Model" button
- Wait for training to complete
- Model will be saved automatically

#### Step 3: Predict Fights
- Go to "🥊 Fight Predictor" page
- Select two fighters from dropdowns
- Choose weight class
- Click "🎯 Predict Winner"
- View prediction results with probabilities

#### Step 4: Ask Questions
- Go to "💬 Ask Questions" page
- Type your question or click example questions
- Get instant answers about UFC data

## 💡 Example Questions You Can Ask

### Fighter Statistics
- "Who has the most wins?"
- "Who has the highest win rate?"
- "What is Conor McGregor's record?"
- "How many fights has Jon Jones had?"
- "List top 10 fighters by wins"

### Fighter Comparisons
- "Compare Jon Jones vs Daniel Cormier"
- "Compare Khabib Nurmagomedov vs Conor McGregor"

### Physical Attributes
- "Who has the longest reach?"
- "What is the average height of fighters?"

### Event Information
- "How many events have been held?"
- "What are the most common weight classes?"

### ❌ Out of Context Questions
The system will detect and reject questions not related to UFC data:
- "What's the weather today?" ❌
- "How to cook pasta?" ❌
- "Tell me about football" ❌

## 🎨 UI Features

- **Dark UFC Theme**: Professional octagon-inspired design
- **Background Images**: Dynamic UFC wallpapers
- **Smooth Animations**: Button hover effects and transitions
- **Responsive Layout**: Works on all screen sizes
- **Real-time Updates**: Live data preview and predictions

## 🔧 Troubleshooting

### Port Already in Use
If you see "Port 8501 is not available", try:
```bash
streamlit run app.py --server.port 8502
```

### Missing Data
If predictions don't work:
1. Make sure you scraped data first
2. Train the model before predicting
3. Check that CSV files exist in `data/` folder

### Slow Scraping
- Scraping all data takes 5-10 minutes
- Be patient, it's downloading from UFC Stats website
- Don't close the browser during scraping

## 📊 Model Performance

- **Algorithm**: Gradient Boosting Classifier
- **Accuracy**: ~65-70% on historical data
- **Features**: 16 engineered features
- **Training Time**: 2-3 minutes on average dataset

## 🌐 Deployment

To deploy on Streamlit Cloud:
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Set entrypoint to `app.py`
4. Deploy!

## 📝 Notes

- First time setup requires data scraping
- Model training is one-time (unless you want to retrain)
- Predictions are based on historical data patterns
- Q&A system uses rule-based matching for accuracy
