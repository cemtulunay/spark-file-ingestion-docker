### Overview
This project implements a **distributed batch data pipeline using Apache Spark (PySpark)** to process Formula 1 drivers’ lap times from a CSV file.

The pipeline:
- Reads lap time data from CSV
- Validates and cleans the input
- Computes per-driver statistics (average and fastest lap times)
- Ranks drivers by lowest average lap time
- Outputs the **top N drivers** as JSON

The solution follows production-style Spark engineering practices, ensuring:
- Scalable execution on large datasets
- Minimal driver memory usage
- Clear separation of ingestion, transformation, and orchestration logic

---

### Why Spark?
The solution was intentionally implemented using **PySpark** instead of pure Python to:
- Demonstrate distributed data processing skills
- Avoid driver-side bottlenecks for large inputs
- Reflect real-world data engineering pipelines

Only the **final reduced result (top N drivers)** is collected to the driver for CLI output, which is safe and intentional.

---

### Assumptions
- Input data is provided as a CSV file (local or distributed filesystem)
- Lap times are numeric values in seconds
- Lower lap time indicates better performance
- Data is synthetic and fabricated for assessment purposes
- Each driver has multiple lap times
- The job runs as a batch Spark application

---

### Project Structure

```text
pyspark_ingestion/
  io/
    read.py            # Spark CSV ingestion
  transforms/
    clean.py           # Validation and aggregations
  utils/
    spark.py           # SparkSession creation
    logging.py         # Logging setup
  cli.py               # Spark CLI entry point
tests/
  test_transforms.py
data/
  lap_times.csv
requirements.txt
README.md
```

---

### How to Run
Prerequisites
- Python 3.9+
- Java 8 or 11
- Apache Spark (local mode is sufficient)


macOS / Linux
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```
```
python -m pyspark_ingestion.cli \
  --input data/lap_times.csv \
  --master local[*]
```
Windows (PowerShell)
```
python -m venv .venv
```
```
.venv\Scripts\Activate.ps1
```
```
pip install -r requirements.txt
```
```
python -m pyspark_ingestion.cli `
  --input data/lap_times.csv `
  --master local[*]
```
CSV Without Header

If the input CSV does not contain a header row:
```
python -m pyspark_ingestion.cli \
  --input data/lap_times.csv \
  --no-header \
  --columns Driver Time \
  --master local[*]
```

---

### Output

The program outputs JSON to stdout containing the top N drivers ordered by lowest average lap time.\
Example:

```json
[
  {
    "driver": "Hamilton",
    "average_lap_time": 71.234,
    "fastest_lap_time": 69.882
  },
  {
    "driver": "Verstappen",
    "average_lap_time": 71.981,
    "fastest_lap_time": 70.102
  }
]
```

---

### Execution Model
- All heavy computation (validation, aggregation, ranking) runs distributed on Spark executors
- Only the small top-N result is collected to the driver for JSON output
- No large datasets are materialized on the driver

---

### How to Test
macOS / Linux

```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```
```
pytest
```

Windows
```
.venv\Scripts\Activate.ps1
```
```
pip install -r requirements.txt
```
```
pytest
```

---

Notes
- The application can be easily adapted to write results to Parquet, Hive, or a database instead of stdout
- Spark configuration can be tuned via spark-submit for non-local deployments
