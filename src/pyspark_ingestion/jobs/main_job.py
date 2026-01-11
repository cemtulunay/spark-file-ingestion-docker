import argparse
import json
import sys
from pyspark.sql import DataFrame

from pyspark_ingestion.utils.logging import setup_logging, get_logger
from pyspark_ingestion.utils.spark import get_spark
from pyspark_ingestion.io.read import read_lap_times_csv
from pyspark_ingestion.transforms.clean import validate_df, compute_driver_stats, top_n_by_average


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process F1 lap times and return top drivers by average lap time (PySpark)."
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

    parser.add_argument(
        "--n",
        type=int,
        default=3,
        help="Top N drivers to return (default: 3)",
    )

    parser.add_argument(
        "--master",
        default=None,
        help="Spark master, e.g. local[*]. If omitted, uses Spark defaults.",
    )

    return parser.parse_args()


def _df_is_empty(df: DataFrame) -> bool:
    # Efficient-ish emptiness check in Spark: try to fetch 1 row
    return len(df.take(1)) == 0


def main() -> None:
    setup_logging()
    log = get_logger(__name__)
    args = parse_args()

    spark = None
    try:
        spark = get_spark(app_name="your_project_f1_lap_times", master=args.master)

        df = read_lap_times_csv(
            spark=spark,
            csv_path=args.input,
            header=not args.no_header,
            columns=args.columns,
        )

        if _df_is_empty(df):
            raise ValueError("CSV contains no data rows.")

        df_valid = validate_df(df)

        stats_df = compute_driver_stats(df_valid)
        top_df = top_n_by_average(stats_df, n=args.n)

        # Collect the small ranked result to driver JSON output
        rows = top_df.collect()
        print("hello test_feature added here")

        output = [
            {
                "driver": r["driver"],
                "average_lap_time": round(float(r["average_lap_time"]), 3),
                "fastest_lap_time": round(float(r["fastest_lap_time"]), 3),
            }
            for r in rows
        ]

        print(json.dumps(output, indent=2))

    except Exception as e:
        log.error(str(e))
        sys.exit(1)

    finally:
        if spark is not None:
            spark.stop()


if __name__ == "__main__":
    main()