import argparse

from events import write_events_csv
from fighters import write_fighters_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UFC data scraper")
    parser.add_argument(
        "--fighters",
        action="store_true",
        help="Scrape fighters and write ufc_fighters.csv",
    )
    parser.add_argument(
        "--events",
        action="store_true",
        help="Scrape events and write ufc_event_data.csv",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.fighters and not args.events:
        args.fighters = True
        args.events = True

    if args.fighters:
        write_fighters_csv()
    if args.events:
        write_events_csv()


if __name__ == "__main__":
    main()
