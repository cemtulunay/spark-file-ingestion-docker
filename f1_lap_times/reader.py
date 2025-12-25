from __future__ import annotations

import pandas as pd
from typing import List, Optional


def read_lap_times_csv(
    csv_path: str,
    header: bool = True,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Read lap times from a CSV file into a DataFrame.

    Args:
        csv_path: Path to the CSV file.
        header: Whether the CSV file contains a header row.
        columns: Column names to apply if header=False.
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If reading fails or configuration is invalid.
    """
    try:
        if header:
            df = pd.read_csv(csv_path)
        else:
            if not columns:
                raise ValueError(
                    "Column names must be provided when header=False."
                )
            df = pd.read_csv(csv_path, header=None, names=columns)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Input CSV not found: {csv_path}") from e
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {csv_path}") from e

    if df.empty:
        raise ValueError("CSV contains no data rows.")

    return df