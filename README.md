# UFC Data Scraper

This repository contains Python scripts to scrape fighter and event data from [UFC Stats](http://ufcstats.com/).

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run in Browser (Streamlit)

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local URL shown by Streamlit (typically `http://localhost:8501`).

For cloud hosting, set the app entrypoint to `streamlit_app.py`.

## Run in CLI

Run both scrapers:

```bash
python main.py
```

Run only fighters:

```bash
python main.py --fighters
```

Run only events:

```bash
python main.py --events
```

The scripts generate:
- `ufc_fighters.csv`
- `ufc_event_data.csv`
