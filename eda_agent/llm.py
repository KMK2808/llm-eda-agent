from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict, Optional  

from dotenv import load_dotenv
from openai import OpenAI # type: ignore


def generate_extra_eda_snippets(eda_result: "EdaResult", max_snippets: int = 3) -> List[str]: # type: ignore

    client = _get_client()
    summary_text = build_eda_summary_text(eda_result)

    prompt = f"""
You are a senior data analyst using pandas.

Given the following EDA summary, propose up to {max_snippets} short pandas code snippets
for additional exploratory analysis on the DataFrame `df`.

Rules:
- Assume `df` is already defined.
- Do NOT import anything, do NOT read or write files.
- Focus on simple EDA: correlations, groupby summaries, scatter plots, boxplots, etc.
- One snippet per block, no comments.

Return only the code snippets, separated clearly using a line with exactly: ### SNIPPET
Do not add explanations or markdown.
EDA summary:

{summary_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert pandas user writing clean, short code."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content or ""
    # Split on the delimiter
    raw_parts = [part.strip() for part in content.split("### SNIPPET") if part.strip()]
    snippets: List[str] = []
    for part in raw_parts[:max_snippets]:
        snippets.append(part.strip())
    return snippets


def _get_client() -> OpenAI:
    # Load .env once
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

    return OpenAI(api_key=api_key)


def build_eda_summary_text(eda_result: "EdaResult") -> str: # type: ignore
    lines = []

    lines.append(f"CSV path: {eda_result.csv_path}")
    lines.append(f"Rows: {eda_result.n_rows}, Columns: {eda_result.n_cols}")
    lines.append("\nColumn dtypes:")
    for col, dt in eda_result.dtypes.items():
        lines.append(f"- {col}: {dt}")

    lines.append("\nMissing values:")
    for col, cnt in eda_result.missing_counts.items():
        lines.append(f"- {col}: {cnt}")

    lines.append("\nNumeric summary (describe):")
    lines.append(eda_result.describe_numeric.to_string())

    if eda_result.categorical_top_values:
        lines.append("\nCategorical top values:")
        for col, counts in eda_result.categorical_top_values.items():
            lines.append(f"\nColumn: {col}")
            lines.append(counts.to_string())

    return "\n".join(lines)


def generate_llm_insights(eda_result: "EdaResult") -> Optional[str]: # type: ignore

    client = _get_client()
    summary_text = build_eda_summary_text(eda_result)

    prompt = f"""
You are a senior data analyst. You are given summary statistics from an automatic EDA on a tabular dataset.

Your job:
- Highlight 3–6 key observations about the dataset (distribution, ranges, patterns).
- Point out obvious data quality issues (missingness, weird values) and why they matter.
- Suggest 3–5 next analysis steps.

Be concise and practical. Avoid repeating raw numbers unless they support a point.

Here is the EDA summary:

{summary_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful, concise data analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    return content.strip() if content else None
