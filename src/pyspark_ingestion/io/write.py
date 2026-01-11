from __future__ import annotations

from pyspark.sql import DataFrame


def write_parquet(df: DataFrame, output_path: str, mode: str = "overwrite") -> None:
    df.write.mode(mode).parquet(output_path)


def write_json(df: DataFrame, output_path: str, mode: str = "overwrite") -> None:
    df.write.mode(mode).json(output_path)


def write_csv(df: DataFrame, output_path: str, mode: str = "overwrite", header: bool = True) -> None:
    df.write.mode(mode).option("header", str(header).lower()).csv(output_path)
