import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Source: https://stackoverflow.com/a/79781532 (CC BY-SA 4.0)
def catmull_rom_smooth(x: np.ndarray, y: np.ndarray, num_points: int = 50) -> tuple:
    """Return smoothed (xs, ys) through the data using a centripetal Catmull-Rom spline."""
    pts = list(zip(x, y))

    def _segment(P0, P1, P2, P3, n, alpha=0.5):
        def tj(ti, pi, pj):
            dx, dy = pj[0] - pi[0], pj[1] - pi[1]
            return ti + (dx ** 2 + dy ** 2) ** (alpha / 2)
        t0 = 0.0
        t1 = tj(t0, P0, P1)
        t2 = tj(t1, P1, P2)
        t3 = tj(t2, P2, P3)
        if t1 == t0 or t2 == t1 or t3 == t2 or t2 == t0 or t3 == t1:
            return np.array([P1] * n)
        t = np.linspace(t1, t2, n).reshape(n, 1)
        P0, P1, P2, P3 = (np.array(p) for p in (P0, P1, P2, P3))
        A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
        A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
        A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3
        B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
        B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
        return (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2

    # Extend with phantom points so the curve reaches the first and last data points
    xbeg = pts[0][0] - (pts[1][0] - pts[0][0])
    ybeg = pts[0][1] - (pts[1][1] - pts[0][1])
    xend = pts[-1][0] - (pts[-2][0] - pts[-1][0])
    yend = pts[-1][1] - (pts[-2][1] - pts[-1][1])
    pts = [(xbeg, ybeg)] + pts + [(xend, yend)]

    segments = [_segment(pts[i], pts[i+1], pts[i+2], pts[i+3], num_points)
                for i in range(len(pts) - 3)]
    curve = np.concatenate(segments, axis=0)
    return curve[:, 0], curve[:, 1]

plt.style.use("IPEC_Style.mplstyle")

# Folder containing measurement CSV files for Buck Mode
data_folder = "Buck Mode"

# Initialize plot
plt.figure(figsize=(6, 3.5))

found_files = False

# Loop through all CSV files in the folder
for filename in os.listdir(data_folder):
    if filename.lower().endswith(".csv"):
        found_files = True
        filepath = os.path.join(data_folder, filename)

        # Find the row that contains the data header (Yokogawa WT format)
        skip_rows = 0
        with open(filepath, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if line.startswith("Store No."):
                    skip_rows = i
                    break

        df = pd.read_csv(filepath, sep=';', skiprows=skip_rows, decimal=',')

        # Strip whitespace from column names and string values
        df.columns = df.columns.str.strip()

        # Try to find the right columns
        power_col = [c for c in df.columns if "P-E2" in c]
        eff_col   = [c for c in df.columns if "etaNurBk" in c]

        if power_col and eff_col:
            x = pd.to_numeric(df[power_col[0]], errors='coerce')
            y = pd.to_numeric(df[eff_col[0]],   errors='coerce')
            mask = x.notna() & y.notna()
            x, y = x[mask].to_numpy(), y[mask].to_numpy()
            label = filename.rsplit(".", 1)[0]
            color = plt.gca()._get_lines.get_next_color()
            # Scatter markers at actual measurement points
            plt.scatter(x, y, s=15, color=color, zorder=3)
            # Smooth centripetal Catmull-Rom spline through the points
            xs, ys = catmull_rom_smooth(x, y, num_points=50)
            plt.plot(xs, ys, color=color, label=label)
        else:
            print(f"WARNING: Could not find columns in {filename}")
            print(f"  Available columns: {df.columns.tolist()}")

if not found_files:
    print(f"No CSV files found in '{os.path.abspath(data_folder)}'")

plt.xlabel(r'$P_\mathrm{out}$ [W]')
plt.ylabel(r'Efficiency [\unit{\percent}]') 
#plt.title("Efficiency vs Output Power (Buck Mode)")
plt.ylim(90, 98)
plt.xlim(0, 1000)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()