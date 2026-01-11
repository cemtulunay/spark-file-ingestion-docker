import pytest
from pyspark.sql import SparkSession

from src.pyspark_ingestion.transforms.clean import validate_df, compute_driver_stats, top_n_by_average


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").appName("test").getOrCreate()


def test_pipeline_happy_path(spark):
    df = spark.createDataFrame(
        [
            ("Hamilton", "90.1"),
            ("Hamilton", "89.9"),
            ("Verstappen", "90.0"),
            ("Verstappen", "90.2"),
            ("Leclerc", "91.0"),
            ("Leclerc", "90.8"),
        ],
        ["Driver", "Time"],
    )

    cleaned = validate_df(df)
    stats = compute_driver_stats(cleaned)
    top = top_n_by_average(stats, n=2).collect()

    assert len(top) == 2
    assert top[0]["driver"] in ("Hamilton", "Verstappen", "Leclerc")
    assert top[0]["driver"] == "Hamilton"
    assert top[1]["driver"] == "Verstappen"
