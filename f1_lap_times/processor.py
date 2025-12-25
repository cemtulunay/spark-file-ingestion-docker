from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class DriverStats:
    driver: str
    average_lap_time: float
    fastest_lap_time: float


def validate_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the input DataFrame.
    """
    try:
        out = df[["Driver", "Time"]].copy()
    except KeyError as e:
        raise ValueError("Missing required columns: Driver, Time") from e

    try:
        out["Driver"] = out["Driver"].astype(str).str.strip()
        out["Time"] = pd.to_numeric(out["Time"], errors="raise")
    except Exception as e:
        raise ValueError("Failed to cast Driver or Time columns") from e

    if (out["Driver"] == "").any():
        raise ValueError("Found empty Driver value(s).")

    if (out["Time"] <= 0).any():
        raise ValueError("Found non-positive Time value(s).")

    return out


def compute_driver_stats(df: pd.DataFrame) -> list[DriverStats]:
    """
    Compute average and fastest lap times per driver.
    """
    try:
        grouped = (
            df.groupby("Driver", as_index=False)["Time"]
            .agg(average_lap_time="mean", fastest_lap_time="min")
        )
    except Exception as e:
        raise RuntimeError("Failed to aggregate driver statistics") from e

    return [
        DriverStats(
            driver=row["Driver"],
            average_lap_time=float(row["average_lap_time"]),
            fastest_lap_time=float(row["fastest_lap_time"]),
        )
        for _, row in grouped.iterrows()
    ]

def top_n_by_average(stats: list[DriverStats], n: int = 3) -> list[DriverStats]:
    """
    Sort by ascending average lap time and return top N drivers.
    """
    try:
        return sorted(
            stats,
            key=lambda s: (s.average_lap_time, s.fastest_lap_time, s.driver.lower()),
        )[:n]
    except Exception as e:
        raise RuntimeError("Failed to rank driver statistics") from e