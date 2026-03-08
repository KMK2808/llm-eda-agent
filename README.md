***

# EDA Agent – CLI EDA Report Generator (V1)

A minimal command-line tool that runs **automatic exploratory data analysis (EDA)** on a CSV file and produces a **Markdown report** with basic statistics and plots.

## Features

- Load any CSV into pandas.
- Compute:
  - Rows and columns.
  - Column data types.
  - Missing value counts per column.
  - Descriptive statistics for numeric columns.
  - Top values for up to 5 categorical columns.
- Generate histogram plots for all numeric columns.
- Save a readable **Markdown report** with embedded plots.
- (V2) Optional LLM-generated **Automated Insights** section:
  - Summarizes key patterns in the data.
  - Highlights data quality issues.
  - Suggests next analysis steps.
- (V3) LLM-suggested **extra EDA code snippets**:
  - Model proposes up to 3 pandas snippets using `df`.
  - Tool executes them and logs success/errors in the report.


## Project structure

```text
eda_agent_project/
  data/
    sample.csv
    ...
  eda_agent/
    __init__.py
    cli.py
    eda.py
    report.py
  reports/
    ...
  requirements.txt
  README.md
```

## Installation

1. Clone or copy this project.  
2. Create and activate a virtual environment:

```bash
cd eda_agent_project
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run from the project root:

```bash
python -m eda_agent.cli --csv_path data\sample.csv --output_dir reports\sample
```

Arguments:

- `--csv_path` (required): Path to the input CSV file.  
- `--output_dir` (optional): Directory where the report and plots will be saved (default: `reports`).

After running, you will get:

- `eda_report.md` – Markdown EDA report.  
- One or more `hist_<column>.png` histogram images.

Open `eda_report.md` in any Markdown viewer (e.g., VS Code) to see the full report.

## Example

Using the Kaggle Titanic dataset:

```bash
python -m eda_agent.cli --csv_path data\titanic\train.csv --output_dir reports\titanic
```

This creates `reports/titanic/eda_report.md` with:

- Dataset shape and schema.  
- Missing values per column.  
- Numeric summary for features like `Age`, `Fare`, etc.  
- Top categories for columns like `Sex`, `Embarked`.  
- Histograms for each numeric feature.

***

## Versions

- **V1** – CLI-based automatic EDA (Markdown report + plots, no LLM).
- **V2** – Added LLM narrative section ("Automated Insights") using OpenAI.
- **V3** – Added LLM-suggested extra analyses (pandas code snippets with execution status).
