import argparse
from pathlib import Path

from .eda import run_basic_eda
from .report import generate_report

VALID_PROFILES = ["general", "data_quality", "feature_engineering"]

def main():
    parser = argparse.ArgumentParser(description="LLM-powered EDA Agent")
    parser.add_argument("--csv_path", required=True, help="Path to input CSV file")
    parser.add_argument("--output_dir", default="reports", help="Output directory for report")
    parser.add_argument(
        "--profile",
        default="general",
        choices=VALID_PROFILES,
        help="EDA profile: general | data_quality | feature_engineering",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running EDA on: {csv_path} [profile: {args.profile}]")
    eda_result = run_basic_eda(csv_path, output_dir, profile=args.profile)

    report_path = generate_report(eda_result, output_dir)
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    main()
