import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

# Output directory
OUTPUT_DIR = Path("data/cicids2017/reports/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CIC-IDS2017 Wednesday dataset: original distribution
original = {
    "BENIGN": 440031,
    "DoS Hulk": 231073,
    "DoS GoldenEye": 10293,
    "DoS slowloris": 5796,
    "DoS Slowhttptest": 5499,
    "Heartbleed": 11
}

# Distribution after cleaning
cleaned = {
    "BENIGN": 420900,
    "DoS Hulk": 177540,
    "DoS GoldenEye": 10293,
    "DoS slowloris": 5548,
    "DoS Slowhttptest": 5499,
    "Heartbleed": 11
}

# ==========================================
# CHART 1: BENIGN VS MALICIOUS TRAFFIC
# ==========================================

benign = original["BENIGN"]
malicious = sum(
    count for label, count in original.items()
    if label != "BENIGN"
)

plt.figure(figsize=(9, 6))

labels = ["Benign traffic", "Malicious traffic"]
values = [benign, malicious]

bars = plt.bar(labels, values)

plt.title(
    "CIC-IDS2017 Wednesday: Benign vs Malicious Traffic",
    fontsize=14
)
plt.ylabel("Number of network flows")
plt.grid(axis="y", alpha=0.3)

total = sum(values)

for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:,}\n({value / total * 100:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "01_benign_vs_malicious.png",
    dpi=300
)
plt.close()


# ==========================================
# CHART 2: TRAFFIC CLASS DISTRIBUTION
# ==========================================

labels = list(original.keys())
values = list(original.values())

plt.figure(figsize=(11, 7))

bars = plt.barh(labels, values)

plt.title(
    "CIC-IDS2017 Wednesday: Traffic Class Distribution",
    fontsize=14
)
plt.xlabel("Number of network flows")
plt.grid(axis="x", alpha=0.3)

for bar, value in zip(bars, values):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {value:,}",
        va="center"
    )

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "02_traffic_class_distribution.png",
    dpi=300
)
plt.close()


# ==========================================
# CHART 3: BEFORE VS AFTER CLEANING
# ==========================================

comparison = pd.DataFrame({
    "Original": original,
    "Cleaned": cleaned
})

ax = comparison.plot(
    kind="bar",
    figsize=(12, 7)
)

ax.set_title(
    "CIC-IDS2017 Wednesday: Before vs After Cleaning",
    fontsize=14
)
ax.set_xlabel("Traffic class")
ax.set_ylabel("Number of network flows")
ax.grid(axis="y", alpha=0.3)
ax.legend(title="Dataset")

plt.xticks(rotation=25, ha="right")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "03_before_after_cleaning.png",
    dpi=300
)
plt.close()


# ==========================================
# SUMMARY
# ==========================================

print("\nVisualization completed successfully!")

print("\nGenerated files:")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print(f"{file} ({file.stat().st_size / 1024:.1f} KB)")
