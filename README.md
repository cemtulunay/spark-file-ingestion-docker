# Resources for Data Engineering Interview

At this point, you shared your GitHub handle and have access this repo.

Now do this:
1. Fork this repository
1. Provide access to the following GitHub user:
    1. `jagnbcuni`
2. Once you complete the General assessment and your specific assessment, commit your changes to your forked repo
3. Please send your recuriter the link to your repo (we won't receive the GitHub's invite email).

### General Assessment
Please complete the [skills self-assessment](./general/skill-self-assessment.md).

### Engineering Specific Assessment
Please complete [this offline assessment](./engineering/formula-1.md)

### Visualization Specific Assessment
Only if directed, please download [this assessment](./visualization/peacock-de-eval.tar.gz) and follow the instructions contained inside.

---

## Solution – F1 Lap Time Processing

### Overview
This project implements a simple batch data pipeline that processes
Formula 1 drivers’ lap times from a CSV file, computes average and
fastest lap times per driver, and outputs the top three drivers ranked
by lowest average lap time.

The solution is designed to be easy to read, test, and run from the
command line, following production-style engineering practices.

---

### Assumptions
- Input data is provided as a single CSV file.
- The CSV contains lap times in seconds.
- Lower lap time indicates better performance.
- Data is synthetic and fabricated for assessment purposes.
- Each driver has at least 3 lap times.
- The process runs as a batch job on a single file.

---

### Project Structure

```text
f1_lap_times/
  reader.py        # CSV ingestion
  processor.py     # Validation, aggregation, ranking
  cli.py           # Command-line entry point
tests/
  test_reader.py
  test_processor.py
data/
  lap_times.csv
requirements.txt
README.md
```

---

### How to Run

From the repository root, run the batch pipeline using:

#### macOS / Linux

```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
python -m f1_lap_times.cli --input data/lap_times.csv
```

#### Windows
```PowerShell
python -m venv .venv
```
```PowerShell
.venv\Scripts\Activate.ps1
```
```PowerShell
pip install -r requirements.txt
```
```PowerShell
python -m f1_lap_times.cli --input data/lap_times.csv
```

Where there is no header on data file replace the run parameter
```markdown
python -m f1_lap_times.cli \
  --input data/lap_times.csv \
  --no-header \
  --columns Driver Time
```

---

### Output

The program outputs JSON containing the top three drivers ordered by lowest average lap time. Each entry includes the driver name, average lap time, and fastest lap time.

---

### How to Test
#### macOS / Linux
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
pytest
```
#### Windows
```PowerShell
.venv\Scripts\Activate.ps1
```
```PowerShell
pip install -r requirements.txt
```
```PowerShell
pytest
```