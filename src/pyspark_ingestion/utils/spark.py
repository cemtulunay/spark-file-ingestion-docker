from __future__ import annotations

from pyspark.sql import SparkSession


def get_spark(app_name: str, master: str | None = None) -> SparkSession:
    builder = SparkSession.builder.appName(app_name)
    if master:
        builder = builder.master(master)

    spark = builder.getOrCreate()
    return spark
