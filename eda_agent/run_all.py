from pathlib import Path
import subprocess
import sys

def main():
    data_dir = Path(__file__).resolve().parents[1] / "data"
    profiles = ["general", "data_quality", "feature_engineering"]

    csv_files = list(data_dir.rglob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/")
        sys.exit(1)

    for csv_path in csv_files:
        for profile in profiles:
            output_dir = Path(__file__).resolve().parents[1] / "reports" / f"{csv_path.stem}_{profile}"
            print(f"\nRunning: {csv_path.name} | profile: {profile}")
            subprocess.run([
                sys.executable,  # ← this uses the current venv Python, not system Python
                "-m", "eda_agent.cli",
                "--csv_path", str(csv_path),
                "--output_dir", str(output_dir),
                "--profile", profile,
            ])

if __name__ == "__main__":
    main()
