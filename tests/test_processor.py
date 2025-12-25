import pandas as pd
import pytest

from f1_lap_times.processor import (
    validate_df,
    compute_driver_stats,
    top_n_by_average,
)

"""
Tests for data validation and aggregation logic in processor.py.
"""

# Valid input survives validation
def test_validate_df_valid_data_passes():
    df = pd.DataFrame(
        {
            "Driver": ["Alonso", "Hamilton"],
            "Time": [4.32, 4.65],
        }
    )

    validated = validate_df(df)

    assert len(validated) == 2
    assert list(validated.columns) == ["Driver", "Time"]

# Missing required columns raises an error
def test_validate_df_missing_columns_fails():
    df = pd.DataFrame(
        {
            "Driver": ["Alonso"],
        }
    )

    with pytest.raises(ValueError):
        validate_df(df)

# Non-numeric time raises an error
def test_validate_df_invalid_time_fails():
    df = pd.DataFrame(
        {
            "Driver": ["Alonso"],
            "Time": ["not_a_number"],
        }
    )

    with pytest.raises(ValueError):
        validate_df(df)

# Aggregation logic produces correct average and fastest lap
def test_compute_driver_stats_calculates_average_and_fastest():
    df = pd.DataFrame(
        {
            "Driver": ["Alonso", "Alonso", "Hamilton"],
            "Time": [4.32, 4.38, 4.65],
        }
    )

    stats = compute_driver_stats(df)

    alonso = next(s for s in stats if s.driver == "Alonso")

    assert round(alonso.average_lap_time, 2) == 4.35
    assert alonso.fastest_lap_time == 4.32

# Tests that drivers are correctly ranked by lowest average lap time.
def test_top_n_by_average_returns_top_three_sorted():
    df = pd.DataFrame(
        {
            "Driver": ["A", "A", "B", "B", "C", "C", "D", "D"],
            "Time":   [4.0, 4.2, 4.5, 4.6, 3.9, 4.1, 5.0, 5.1],
        }
    )

    stats = compute_driver_stats(df)
    top_three = top_n_by_average(stats, n=3)

    drivers = [d.driver for d in top_three]

    # Expected order by lowest average lap time
    assert drivers == ["C", "A", "B"]
