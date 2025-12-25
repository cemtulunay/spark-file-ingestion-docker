import argparse
import json
import logging
import sys

from f1_lap_times.reader import read_lap_times_csv
from f1_lap_times.processor import (
    validate_df,
    compute_driver_stats,
    top_n_by_average,
)

"""
This CLI acts as the entry point for the batch pipeline.
It allows the entire process (read, validate, aggregate, rank)
to be executed with a single command, without depending on an IDE.
"""

# Configures how log messages look and what level gets printed
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

# Reads what the user typed in the command line and turns it into variables pipeline program can use
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process F1 lap times and return top drivers by average lap time."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV file containing lap times",
    )

    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Specify if the CSV file does not contain a header row",
    )

    parser.add_argument(
        "--columns",
        nargs="+",
        help="Column names to use when --no-header is set (e.g. Driver Time)",
    )

    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    try:
        df = read_lap_times_csv(
            csv_path=args.input,
            header=not args.no_header,
            columns=args.columns,
        )

        df = validate_df(df)

        stats = compute_driver_stats(df)
        top_drivers = top_n_by_average(stats, n=3)

        output = [
            {
                "driver": s.driver,
                "average_lap_time": round(s.average_lap_time, 3),
                "fastest_lap_time": round(s.fastest_lap_time, 3),
            }
            for s in top_drivers
        ]

        print(json.dumps(output, indent=2))

    except Exception as e:
        logging.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
