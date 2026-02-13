import csv
from typing import List
import requests
from bs4 import BeautifulSoup


def scrape_fighter_data(char: str) -> List[List[str]]:
    url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    fighters = []
    fighter_table = soup.find("table", class_="b-statistics__table")
    if fighter_table is None:
        return fighters

    rows = fighter_table.find_all("tr")[2:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 10:
            continue

        fighters.append([
            cols[0].text.strip(),  # First Name
            cols[1].text.strip(),  # Last Name
            cols[2].text.strip(),  # Nickname
            cols[3].text.strip(),  # Height
            cols[4].text.strip(),  # Weight
            cols[5].text.strip(),  # Reach
            cols[6].text.strip(),  # Stance
            cols[7].text.strip(),  # Wins
            cols[8].text.strip(),  # Losses
            cols[9].text.strip(),  # Draws
        ])

    return fighters


def write_fighters_csv(output_path: str = "ufc_fighters.csv") -> None:
    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["First Name", "Last Name", "Nickname", "Height", "Weight", "Reach", "Stance", "Wins", "Losses", "Draws"])
        
        for char in "abcdefghijklmnopqrstuvwxyz":
            fighters = scrape_fighter_data(char)
            writer.writerows(fighters)
