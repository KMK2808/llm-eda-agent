from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt  # type: ignore

from .llm import generate_extra_eda_snippets


@dataclass
class EdaResult:
    csv_path: Path
    output_dir: Path
    n_rows: int
    n_cols: int
    dtypes: Dict[str, str]
    missing_counts: Dict[str, int]
    describe_numeric: pd.DataFrame
    plots: Dict[str, Path]
    categorical_top_values: Dict[str, Series]
    extra_analyses: List[Dict[str, Optional[str]]]


def run_basic_eda(csv_path: Path, output_dir: Path) -> EdaResult:
    df = pd.read_csv(csv_path)

    n_rows, n_cols = df.shape
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    missing_counts = df.isna().sum().to_dict()
    describe_numeric = df.select_dtypes(include="number").describe()

    plots: Dict[str, Path] = {}

    numeric_cols = list(df.select_dtypes(include="number").columns)
    for col in numeric_cols:
        plt.figure()
        df[col].hist(bins=30)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        hist_path = output_dir / f"hist_{col}.png"
        plt.savefig(hist_path, bbox_inches="tight")
        plt.close()
        plots[f"hist_{col}"] = hist_path

    # Categorical summary
    categorical_top_values: Dict[str, Series] = {}
    categorical_cols = list(df.select_dtypes(exclude="number").columns)
    for col in categorical_cols[:5]:
        counts = df[col].value_counts(dropna=False).head(10)
        categorical_top_values[col] = counts

    # LLM-suggested extra analyses (code snippets)
    extra_analyses: List[Dict[str, Optional[str]]] = []
    try:
        temp_result = EdaResult(
            csv_path=csv_path,
            output_dir=output_dir,
            n_rows=n_rows,
            n_cols=n_cols,
            dtypes=dtypes,
            missing_counts=missing_counts,
            describe_numeric=describe_numeric,
            plots=plots,
            categorical_top_values=categorical_top_values,
            extra_analyses=[],
        )
        snippets = generate_extra_eda_snippets(temp_result)
    except Exception as e:
        snippets = []
        extra_analyses.append(
            {
                "code": None,
                "status": "error_initial",
                "error": f"Failed to get extra EDA snippets from LLM: {e}",
            }
        )

    exec_env = {"df": df.copy(), "plt": plt}
    for code in snippets:
        result: Dict[str, Optional[str]] = {"code": code, "status": None, "error": None}
        try:
            exec(code, {}, exec_env)
            result["status"] = "success"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        extra_analyses.append(result)

    return EdaResult(
        csv_path=csv_path,
        output_dir=output_dir,
        n_rows=n_rows,
        n_cols=n_cols,
        dtypes=dtypes,
        missing_counts=missing_counts,
        describe_numeric=describe_numeric,
        plots=plots,
        categorical_top_values=categorical_top_values,
        extra_analyses=extra_analyses,
    )
