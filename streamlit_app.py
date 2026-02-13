from pathlib import Path

import pandas as pd
import requests
import streamlit as st

from events import write_events_csv
from fighters import write_fighters_csv


st.set_page_config(page_title="UFC Data Scraper", layout="wide")

BASE_DIR = Path(__file__).parent
FIGHTERS_CSV = BASE_DIR / "ufc_fighters.csv"
EVENTS_CSV = BASE_DIR / "ufc_event_data.csv"


def show_csv_preview(csv_path: Path, title: str, rows: int = 25) -> None:
    if not csv_path.exists():
        st.info(f"{title} file not found yet.")
        return

    df = pd.read_csv(csv_path)
    st.subheader(title)
    st.caption(f"Rows: {len(df):,}")
    st.dataframe(df.head(rows), use_container_width=True)
    st.download_button(
        label=f"Download {csv_path.name}",
        data=csv_path.read_bytes(),
        file_name=csv_path.name,
        mime="text/csv",
    )


def main() -> None:
    st.title("UFC Data Scraper")
    st.write("Run fighter and event scraping from this page and download generated CSV files.")

    left, right = st.columns(2)

    with left:
        st.subheader("Fighters")
        if st.button("Scrape Fighters", use_container_width=True):
            try:
                with st.spinner("Scraping fighters..."):
                    write_fighters_csv(str(FIGHTERS_CSV))
                st.success(f"Saved {FIGHTERS_CSV.name}")
            except requests.RequestException as exc:
                st.error(f"Network error while scraping fighters: {exc}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Failed to scrape fighters: {exc}")

    with right:
        st.subheader("Events")
        if st.button("Scrape Events", use_container_width=True):
            try:
                with st.spinner("Scraping events..."):
                    write_events_csv(str(EVENTS_CSV))
                st.success(f"Saved {EVENTS_CSV.name}")
            except requests.RequestException as exc:
                st.error(f"Network error while scraping events: {exc}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Failed to scrape events: {exc}")

    st.divider()
    preview_rows = st.slider("Preview rows", min_value=5, max_value=100, value=25, step=5)
    cols1, cols2 = st.columns(2)
    with cols1:
        show_csv_preview(FIGHTERS_CSV, "Fighters Preview", rows=preview_rows)
    with cols2:
        show_csv_preview(EVENTS_CSV, "Events Preview", rows=preview_rows)


if __name__ == "__main__":
    main()
