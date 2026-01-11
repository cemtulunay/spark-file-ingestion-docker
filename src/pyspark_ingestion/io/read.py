from __future__ import annotations

from typing import List, Optional
from pyspark.sql import SparkSession, DataFrame


def read_lap_times_csv(
    spark: SparkSession,
    csv_path: str,
    header: bool = True,
    columns: Optional[List[str]] = None,
) -> DataFrame:
    """
    Read lap times from a CSV file into a Spark DataFrame.

    This is intentionally strict-ish:
    - Reads all columns as strings initially
    - FAILFAST on malformed rows
    - Lets validate_df handle casting and validation rules

    Args:
        spark: SparkSession
        csv_path: Path to the CSV file.
        header: Whether the CSV file contains a header row.
        columns: Column names to apply if header=False.
    Raises:
        ValueError: If reading fails or configuration is invalid.
    """
    try:
        reader = (
            spark.read.format("csv")
            .option("mode", "FAILFAST")
            .option("header", "true" if header else "false")
            .option("inferSchema", "false")  # keep as strings first
        )

        df = reader.load(csv_path)

        if not header:
            if not columns:
                raise ValueError("Column names must be provided when header=False.")

            # Spark names columns _c0, _c1... when header=False
            if len(columns) > len(df.columns):
                raise ValueError(
                    f"Provided {len(columns)} column names but file has only {len(df.columns)} columns."
                )

            for i, name in enumerate(columns):
                df = df.withColumnRenamed(f"_c{i}", name)

        return df

    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {csv_path}") from e