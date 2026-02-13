import csv
import re
from typing import List
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_event_urls() -> List[str]:
    url = "http://ufcstats.com/statistics/events/completed?page=all"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    event_links = [a["href"] for a in soup.select("td.b-statistics__table-col a")]
    return event_links[1:]


def scrape_fight_data(event_url: str) -> List[List[str]]:
    response = requests.get(event_url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    fights = []

    event_name_tag = soup.find("h2", class_="b-content__title")
    event_date_tag = soup.find("li", class_="b-list__box-list-item")
    fight_table = soup.find("table", class_="b-fight-details__table")
    if event_name_tag is None or event_date_tag is None or fight_table is None:
        return fights

    event_name = event_name_tag.text.strip()
    event_date = event_date_tag.text.strip().split("\n")[-1].strip()
    rows = fight_table.find_all("tr", class_="b-fight-details__table-row")[1:]

    for row in rows:
        cols = row.find_all("td", recursive=False)
        if len(cols) < 10:
            continue

        result_tag = cols[0].find("i", class_="b-flag__inner")
        result = "" if result_tag is None else " ".join(result_tag.text.strip().split())
        fighters = cols[1].find_all("a")
        if len(fighters) < 2:
            continue

        fighter1 = fighters[0].text.strip()
        fighter2 = fighters[1].text.strip()
        winner = fighter1 if result == "win" else ("Draw" if result == "draw" else "Unknown")

        fights.append([
            event_name,
            event_date,
            winner,
            fighter1,
            fighter2,
            re.sub(r"\s+", "-", cols[2].text.strip().replace("\n", "")),  # KD
            re.sub(r"\s+", "-", cols[3].text.strip().replace("\n", "")),  # Strikes
            re.sub(r"\s+", "-", cols[4].text.strip().replace("\n", "")),  # TD
            re.sub(r"\s+", "-", cols[5].text.strip().replace("\n", "")),  # Sub
            cols[6].text.strip(),  # Weight Class
            re.sub(r"\s+", "-", cols[7].text.strip().replace("\n", "")),  # Method
            cols[8].text.strip(),  # Round
            cols[9].text.strip(),  # Time
        ])

    return fights


def write_events_csv(output_path: str = "ufc_event_data.csv") -> None:
    event_urls = get_event_urls()
    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Event Name", "Event Date", "Result", "Fighter1", "Fighter2", "KD", "Strikes", "TD", "Sub", "Weight Class", "Method", "Round", "Time"])
        
        for event_url in tqdm(event_urls, desc="Loading data"):
            fights = scrape_fight_data(event_url)
            writer.writerows(fights)
