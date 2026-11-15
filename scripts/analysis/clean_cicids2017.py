import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = Path(
    "data/cicids2017/raw/MachineLearningCVE/"
    "Wednesday-workingHours.pcap_ISCX.csv"
)

OUTPUT_DIR = Path("data/cicids2017/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "Wednesday-cleaned.csv"

CHUNK_SIZE = 50000

total_input = 0
total_output = 0
invalid_labels = 0
duplicate_rows = 0
missing_before = 0
missing_after = 0

print("Starting CIC-IDS2017 cleaning...")

first_chunk = True
seen_rows = set()

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    total_input += len(chunk)

    # Normalize column names
    chunk.columns = chunk.columns.str.strip()

    # Normalize labels
    chunk["Label"] = chunk["Label"].astype("string").str.strip()

    # Remove rows with missing or empty labels
    valid = chunk["Label"].notna() & chunk["Label"].ne("")
    invalid_labels += int((~valid).sum())
    chunk = chunk.loc[valid].copy()

    # Convert positive and negative infinity to NaN
    numeric_columns = chunk.select_dtypes(include="number").columns
    chunk[numeric_columns] = chunk[numeric_columns].replace(
        [np.inf, -np.inf], np.nan
    )

    missing_before += int(chunk.isna().sum().sum())

    # Remove duplicate records globally using a SHA-256 fingerprint.
    # Exact duplicate rows receive the same fingerprint.
    fingerprints = pd.util.hash_pandas_object(
        chunk, index=False
    )

    keep = ~fingerprints.isin(seen_rows)
    duplicate_rows += int((~keep).sum())

    seen_rows.update(fingerprints[keep].tolist())

    chunk = chunk.loc[keep].copy()

    # Remove rows with missing labels, if any remain
    chunk = chunk.dropna(subset=["Label"])

    # Replace missing numeric feature values with column medians.
    # Median values are calculated from each chunk, so this is a
    # demonstration cleaning strategy, not a global imputation model.
    numeric_columns = chunk.select_dtypes(include="number").columns

    for column in numeric_columns:
        median = chunk[column].median()

        if pd.notna(median):
            chunk[column] = chunk[column].fillna(median)

    missing_after += int(chunk.isna().sum().sum())

    # Append cleaned chunk
    chunk.to_csv(
        OUTPUT_FILE,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False
    total_output += len(chunk)

    print(f"Processed {total_input:,} input records...")

print("\n========== CLEANING SUMMARY ==========")
print(f"Input records: {total_input:,}")
print(f"Output records: {total_output:,}")
print(f"Removed invalid labels: {invalid_labels:,}")
print(f"Removed duplicate records: {duplicate_rows:,}")
print(f"Missing cells before imputation: {missing_before:,}")
print(f"Missing cells after imputation: {missing_after:,}")
print(f"Output file: {OUTPUT_FILE}")

print("\nCleaning completed.")
