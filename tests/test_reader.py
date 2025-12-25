import pandas as pd
import pytest

from f1_lap_times.reader import read_lap_times_csv

"""
Tests for CSV ingestion logic in reader.py.
"""

# checks that a valid CSV file is read correctly into a DataFrame
def test_read_lap_times_csv_reads_valid_file(tmp_path):
    csv_file = tmp_path / "lap_times.csv"
    csv_file.write_text("Driver,Time\nAlonso,4.32\nHamilton,4.65\n", encoding="utf-8")

    df = read_lap_times_csv(str(csv_file))

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["Driver", "Time"]
    assert len(df) == 2

# checks that reading a missing file raises an error
def test_read_lap_times_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        read_lap_times_csv("does_not_exist.csv")

# checks that a CSV without headers can be read when column names are provided
def test_read_lap_times_csv_no_header_with_columns(tmp_path):
    csv_file = tmp_path / "no_header.csv"
    csv_file.write_text("Alonso,4.32\nHamilton,4.65\n", encoding="utf-8")

    df = read_lap_times_csv(
        str(csv_file),
        header=False,
        columns=["Driver", "Time"],
    )

    assert list(df.columns) == ["Driver", "Time"]
    assert len(df) == 2
