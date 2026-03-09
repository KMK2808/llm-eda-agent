# EDA Agent – CLI EDA Report Generator

A command-line tool that runs **automatic exploratory data analysis (EDA)** on a CSV file and produces a **Markdown report** with statistics, plots, and LLM-powered insights.


## Features

- Load any CSV into pandas.
- Compute:
  - Rows and columns.
  - Column data types.
  - Missing value counts per column.
  - Descriptive statistics for numeric columns.
  - Top values for categorical columns.
- Generate histogram plots for all numeric columns.
- Save a readable **Markdown report** with embedded plots.
- (V2) LLM-generated **Automated Insights** section:
  - Summarizes key patterns in the data.
  - Highlights data quality issues.
  - Suggests next analysis steps.
- (V3) LLM-suggested **extra EDA code snippets**:
  - Model proposes up to 3 pandas snippets using `df`.
  - Tool executes them and logs success/errors in the report.
- (V4) Combined numeric histogram grid:
  - All numeric column distributions in one clean grid image.
- (V4) `--profile` flag to steer EDA focus:
  - `general` – balanced overview of distributions, patterns, and data quality.
  - `data_quality` – focuses on missing values, outliers, and inconsistencies.
  - `feature_engineering` – focuses on skewness, encoding opportunities, and feature relationships.
- (V4) Batch runner to process all CSVs across all profiles automatically.

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
    llm.py
    report.py
    run_all.py
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

4. Add your OpenAI API key to a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

## Usage

### Single CSV run

```bash
python -m eda_agent.cli --csv_path data\sample.csv --output_dir reports\sample
```

### Run with a profile

```bash
python -m eda_agent.cli --csv_path data\train.csv --output_dir reports\train_dq --profile data_quality
```

Available profiles: `general` (default), `data_quality`, `feature_engineering`.

### Run all CSVs across all profiles

```bash
python -m eda_agent.run_all
```

This automatically finds every CSV in `data/`, runs all 3 profiles on each, and saves reports to `reports/sv_name>_<profile>/`.

### Arguments

- `--csv_path` (required): Path to the input CSV file.
- `--output_dir` (optional): Directory where the report and plots will be saved (default: `reports`).
- `--profile` (optional): EDA profile – `general`, `data_quality`, or `feature_engineering` (default: `general`).

### Output

- `eda_report.md` – Markdown EDA report with LLM insights and extra analyses.
- `numeric_distributions.png` – Combined histogram grid for all numeric columns.

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
- Combined histogram grid.
- LLM-generated insights and extra pandas analyses.

## Versions

- **V1** – CLI-based automatic EDA (Markdown report + plots, no LLM).
- **V2** – Added LLM narrative section ("Automated Insights") using OpenAI.
- **V3** – Added LLM-suggested extra analyses (pandas code snippets with execution status).
- **V4** – Combined numeric histogram grid, `--profile` flag, and batch runner (`run_all`).
```
