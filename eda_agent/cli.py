import argparse
from pathlib import Path

from .eda import run_basic_eda
from .report import generate_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run basic EDA on a CSV file and generate a report."
    )
    parser.add_argument(
        "--csv_path",
        type=str,
        required=True,
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="reports",
        help="Directory where the report and plots will be saved.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    csv_path = Path(args.csv_path)
    output_dir = Path(args.output_dir)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    eda_result = run_basic_eda(csv_path, output_dir)
    report_path = generate_report(eda_result, output_dir)

    print(f"Report generated at: {report_path}")


if __name__ == "__main__":
    main()
