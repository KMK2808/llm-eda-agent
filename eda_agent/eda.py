from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional
import math

import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from .llm import generate_extra_eda_snippets, generate_llm_insights


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
    profile: str


def run_basic_eda(csv_path: Path, output_dir: Path, profile: str = "general") -> EdaResult:
    df = pd.read_csv(csv_path)

    n_rows, n_cols = df.shape
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    missing_counts = df.isna().sum().to_dict()
    describe_numeric = df.select_dtypes(include="number").describe()

    numeric_cols = list(df.select_dtypes(include="number").columns)

    # --- Combined grid plot ---
    plots: Dict[str, Path] = {}
    if numeric_cols:
        n = len(numeric_cols)
        ncols = 3
        nrows = math.ceil(n / ncols)
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 4 * nrows))
        axes_flat = axes.flatten() if n > 1 else [axes]

        for i, col in enumerate(numeric_cols):
            axes_flat[i].hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="white")
            axes_flat[i].set_title(col, fontsize=11)
            axes_flat[i].set_xlabel(col)
            axes_flat[i].set_ylabel("Frequency")

        # Hide unused subplots
        for j in range(i + 1, len(axes_flat)):
            axes_flat[j].set_visible(False)

        fig.suptitle("Numeric Column Distributions", fontsize=14, fontweight="bold")
        plt.tight_layout()
        grid_path = output_dir / "numeric_distributions.png"
        plt.savefig(grid_path, bbox_inches="tight", dpi=120)
        plt.close()
        plots["numeric_distributions"] = grid_path

    # --- Categorical summary ---
    categorical_top_values: Dict[str, Series] = {}
    categorical_cols = list(df.select_dtypes(exclude="number").columns)

    # data_quality profile: show all categorical columns (up to 10)
    # feature_engineering: show top 3 only
    # general: top 5
    cat_limit = {"general": 5, "data_quality": 10, "feature_engineering": 3}.get(profile, 5)
    for col in categorical_cols[:cat_limit]:
        categorical_top_values[col] = df[col].value_counts(dropna=False).head(10)

    # --- LLM extra analyses ---
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
            profile=profile,
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
        profile=profile,
    )
