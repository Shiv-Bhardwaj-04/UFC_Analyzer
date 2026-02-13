import csv
from typing import List

import requests
from bs4 import BeautifulSoup


def scrape_fighter_data(char: str) -> List[List[str]]:
    """Scrape fighter data for a given starting character."""
    url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    fighters = []
    fighter_table = soup.find("table", class_="b-statistics__table")
    if fighter_table is None:
        return fighters

    rows = fighter_table.find_all("tr")[2:]  # Skip header and blank row.
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 10:
            continue

        first_name = cols[0].text.strip()
        last_name = cols[1].text.strip()
        nickname = cols[2].text.strip()
        height = cols[3].text.strip()
        weight = cols[4].text.strip()
        reach = cols[5].text.strip()
        stance = cols[6].text.strip()
        wins = cols[7].text.strip()
        losses = cols[8].text.strip()
        draws = cols[9].text.strip()

        fighters.append(
            [first_name, last_name, nickname, height, weight, reach, stance, wins, losses, draws]
        )

    return fighters


def write_fighters_csv(output_path: str = "ufc_fighters.csv") -> None:
    """Scrape all fighter rows and save them to CSV."""
    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "First Name",
                "Last Name",
                "Nickname",
                "Height",
                "Weight",
                "Reach",
                "Stance",
                "Wins",
                "Losses",
                "Draws",
            ]
        )

        for char in "abcdefghijklmnopqrstuvwxyz":
            fighters = scrape_fighter_data(char)
            writer.writerows(fighters)


if __name__ == "__main__":
    write_fighters_csv()
