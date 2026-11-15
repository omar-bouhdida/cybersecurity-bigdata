import pandas as pd
from collections import Counter
from pathlib import Path

FILE_PATH = Path(
    "data/cicids2017/raw/MachineLearningCVE/"
    "Wednesday-workingHours.pcap_ISCX.csv"
)

REPORT_DIR = Path("data/cicids2017/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 50000

total_rows = 0
label_counts = Counter()
missing_values = Counter()
duplicate_rows = 0

print("Analyzing CIC-IDS2017 Wednesday dataset...")

for chunk in pd.read_csv(FILE_PATH, chunksize=CHUNK_SIZE):
    chunk.columns = chunk.columns.str.strip()

    total_rows += len(chunk)

    label_counts.update(
        chunk["Label"].astype(str).str.strip().value_counts().to_dict()
    )

    for column, count in chunk.isna().sum().items():
        missing_values[column] += int(count)

    duplicate_rows += int(chunk.duplicated().sum())

# Generate report
report = []

report.append("CIC-IDS2017 DATASET ANALYSIS")
report.append("=" * 45)
report.append(f"Dataset: {FILE_PATH.name}")
report.append(f"Total records: {total_rows:,}")
report.append(f"Total traffic classes: {len(label_counts)}")

report.append("\nTRAFFIC DISTRIBUTION")
report.append("-" * 45)

for label, count in label_counts.most_common():
    percentage = count / total_rows * 100
    report.append(
        f"{label}: {count:,} ({percentage:.2f}%)"
    )

report.append("\nMISSING VALUES")
report.append("-" * 45)
report.append(f"Total missing cells: {sum(missing_values.values()):,}")

for column, count in missing_values.items():
    if count:
        report.append(f"{column}: {count:,}")

report.append("\nDUPLICATES")
report.append("-" * 45)
report.append(
    f"Duplicates within individual chunks: {duplicate_rows:,}"
)

report.append(
    "\nNote: Duplicate detection is limited to individual chunks."
)

report_text = "\n".join(report)

output_file = REPORT_DIR / "wednesday-analysis.txt"
output_file.write_text(report_text, encoding="utf-8")

print("\n" + report_text)
print(f"\nReport saved to: {output_file}")
