from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


REQUIRED_COLS = ("Driver", "Time")


def validate_df(df: DataFrame) -> DataFrame:
    """
    Validate input DataFrame:
    - Requires columns Driver, Time
    - Driver trimmed, must be non-empty
    - Time cast to double, must be > 0
    Returns a cleaned DataFrame with exactly columns: Driver, Time
    """
    cols = set(df.columns)
    missing = [c for c in REQUIRED_COLS if c not in cols]
    if missing:
        raise ValueError("Missing required columns: Driver, Time")

    out = df.select("Driver", "Time")

    # Normalize Driver to trimmed string (null-safe)
    out = out.withColumn("Driver", F.trim(F.coalesce(F.col("Driver").cast("string"), F.lit(""))))

    # Cast Time to numeric; invalid parses become null
    out = out.withColumn("Time", F.col("Time").cast("double"))

    # Empty Driver check
    if out.filter(F.col("Driver") == F.lit("")).limit(1).count() > 0:
        raise ValueError("Found empty Driver value(s).")

    # Invalid/non-positive Time check (null or <= 0)
    if out.filter(F.col("Time").isNull() | (F.col("Time") <= F.lit(0.0))).limit(1).count() > 0:
        raise ValueError("Found non-positive Time value(s).")

    return out


def compute_driver_stats(df: DataFrame) -> DataFrame:
    """
    Compute average and fastest lap times per driver.
    Returns a DataFrame with columns:
      driver, average_lap_time, fastest_lap_time
    """
    try:
        stats = (
            df.groupBy("Driver")
            .agg(
                F.avg("Time").alias("average_lap_time"),
                F.min("Time").alias("fastest_lap_time"),
            )
            .withColumnRenamed("Driver", "driver")
        )
        return stats
    except Exception as e:
        raise RuntimeError("Failed to aggregate driver statistics") from e


def top_n_by_average(stats_df: DataFrame, n: int = 3) -> DataFrame:
    """
    Sort by:
      average_lap_time asc,
      fastest_lap_time asc,
      driver asc (case-insensitive)
    Return top N.
    """
    try:
        ranked = stats_df.orderBy(
            F.col("average_lap_time").asc(),
            F.col("fastest_lap_time").asc(),
            F.lower(F.col("driver")).asc(),
        )
        return ranked.limit(int(n))
    except Exception as e:
        raise RuntimeError("Failed to rank driver statistics") from e
