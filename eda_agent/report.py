from pathlib import Path

from .eda import EdaResult
from .llm import generate_llm_insights


def generate_report(eda_result: EdaResult, output_dir: Path) -> Path:
    report_path = output_dir / "eda_report.md"

    lines = []

    # LLM-based narrative insights
    llm_insights = None
    try:
        llm_insights = generate_llm_insights(eda_result)
    except Exception as e:
        llm_insights = f"(Failed to generate LLM insights: {e})"

    lines.append("# EDA Report\n")

    if llm_insights:
        lines.append("## Automated Insights (LLM)\n")
        lines.append(llm_insights)
        lines.append("")

    lines.append(f"**CSV file:** `{eda_result.csv_path}`\n")
    lines.append(f"**Rows:** {eda_result.n_rows}  ")
    lines.append(f"**Columns:** {eda_result.n_cols}\n")

    lines.append("\n## Column dtypes\n")
    for col, dt in eda_result.dtypes.items():
        lines.append(f"- `{col}`: `{dt}`")

    lines.append("\n## Missing values\n")
    for col, cnt in eda_result.missing_counts.items():
        lines.append(f"- `{col}`: {cnt}")

    lines.append("\n## Numeric summary\n")
    lines.append("```text")
    lines.append(eda_result.describe_numeric.to_string())
    lines.append("```")

    if eda_result.categorical_top_values:
        lines.append("\n## Categorical summary (top values)\n")
        for col, counts in eda_result.categorical_top_values.items():
            lines.append(f"### {col}")
            lines.append("```text")
            lines.append(counts.to_string())
            lines.append("```")

    if eda_result.extra_analyses:
        lines.append("\n## LLM-Suggested Extra Analyses\n")
        for idx, item in enumerate(eda_result.extra_analyses, start=1):
            code = item.get("code")
            status = item.get("status")
            error = item.get("error")

            lines.append(f"### Snippet {idx}")
            if code:
                lines.append("```python")
                lines.append(code)
                lines.append("```")
            else:
                lines.append("_No code available._")

            if status:
                lines.append(f"**Status:** {status}")
            if error:
                lines.append(f"**Error:** `{error}`")
            lines.append("")

    if eda_result.plots:
        lines.append("\n## Plots\n")
        for name, path in eda_result.plots.items():
            rel_path = path.relative_to(output_dir)
            lines.append(f"### {name}")
            lines.append(f"![{name}]({rel_path.as_posix()})\n")

    report_markdown = "\n".join(lines)

    with report_path.open("w", encoding="utf-8") as f:
        f.write(report_markdown)

    return report_path
