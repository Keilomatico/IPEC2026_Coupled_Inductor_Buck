import os
import pandas as pd
import matplotlib.pyplot as plt

# ── Settings ──────────────────────────────────────────────────────────────────
DATA_FOLDER = "Test_Measurement"
TIME_UNIT   = "µs"          # display unit for time axis
TIME_SCALE  = 1e6           # 1 s → 1e6 µs

# ── Load all CSV files ─────────────────────────────────────────────────────────
csv_files = sorted(f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv"))

channels = []
for filename in csv_files:
    path = os.path.join(DATA_FOLDER, filename)

    # Read metadata from the first 11 header rows
    meta = {}
    with open(path) as f:
        for _ in range(11):
            line = f.readline().strip()
            if "," in line:
                key, *vals = line.split(",")
                meta[key.strip()] = vals[0].strip()

    source       = meta.get("Source", filename)
    vertical_unit = meta.get("Vertical Units", "V")

    # Read the numeric data (header is row index 11, i.e. 0-based row 11)
    df = pd.read_csv(path, skiprows=11)
    df.columns = ["time", "value"]

    channels.append({"label": source, "unit": vertical_unit, "df": df})

# ── Plot ───────────────────────────────────────────────────────────────────────
n = len(channels)
fig, axes = plt.subplots(n, 1, figsize=(10, 2.5 * n), sharex=True)
if n == 1:
    axes = [axes]

for ax, ch in zip(axes, channels):
    time_us = (ch["df"]["time"] - ch["df"]["time"].iloc[0]) * TIME_SCALE
    ax.plot(time_us, ch["df"]["value"], linewidth=1)
    ax.set_ylabel(f'{ch["label"]} ({ch["unit"]})')
    ax.grid(True, linestyle="--", alpha=0.5)

axes[-1].set_xlabel(f"Time ({TIME_UNIT})")
t_end = (channels[0]["df"]["time"].iloc[-1] - channels[0]["df"]["time"].iloc[0]) * TIME_SCALE
axes[0].set_xlim(0, t_end)
fig.suptitle("Oscilloscope Measurements", fontsize=13, y=1.01)
fig.tight_layout()
plt.show()
