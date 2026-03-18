import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('IPEC_Style.mplstyle')

# ── Settings ──────────────────────────────────────────────────────────────────
DATA_FOLDER = "2MHz 48V 40A 0.25 DB1-1"
#DATA_FOLDER = "2MHz 48V 0A 0.25 DB1-1 - Meas2"
TIME_UNIT   = "µs"          # display unit for time axis
TIME_SCALE  = 1e6           # 1 s → 1e6 µs
figsize = (6, 3.5)

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

# Helper: time vector shifted to t=0
def time_us(ch):
    return (ch["df"]["time"] - ch["df"]["time"].iloc[0]) * TIME_SCALE

# Channel lookup by source name
ch = {c["label"]: c for c in channels}

color_1 = '#7e2f8eff'   # CH1 & CH3
color_2 = '#0071bcff'   # CH2 & CH4

# ── Load measurement-specific settings from the data folder ───────────────────
import importlib.util, pathlib
_spec = importlib.util.spec_from_file_location(
    "settings", pathlib.Path(DATA_FOLDER) / "settings.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

CH2_offset       = _mod.CH2_offset
CH2_gain         = _mod.CH2_gain
CH4_offset       = _mod.CH4_offset
CH4_gain         = _mod.CH4_gain
VOLTAGE_OFFSET   = _mod.VOLTAGE_OFFSET
CURRENT_SHIFT_US = getattr(_mod, 'CURRENT_SHIFT_US', 0)
CH2_SHIFT_US     = getattr(_mod, 'CH2_SHIFT_US', CURRENT_SHIFT_US)
CH4_SHIFT_US     = getattr(_mod, 'CH4_SHIFT_US', CURRENT_SHIFT_US)
Vin              = _mod.Vin
Deff             = _mod.Deff
fs               = _mod.fs
Lself            = _mod.Lself
k                = _mod.k
X_ZOOM           = getattr(_mod, 'X_ZOOM', 1)
T_START_US       = getattr(_mod, 'T_START_US', None)
T_END_US         = getattr(_mod, 'T_END_US',   None)
X_TICK_SPACING_US = getattr(_mod, 'X_TICK_SPACING_US', None)
X_TICKS_US        = getattr(_mod, 'X_TICKS_US', None)
V_YLIM            = getattr(_mod, 'V_YLIM',   None)
V_YTICKS          = getattr(_mod, 'V_YTICKS', None)
I_YLIM            = getattr(_mod, 'I_YLIM',   None)
I_YTICKS          = getattr(_mod, 'I_YTICKS', None)

delta_I_leg = (Vin * Deff) / (2 * fs * Lself) * (
    2 / (1 + k) * (0.5 - Deff) + 1 / (1 - k)
)
print(f"Expected leg current ripple ΔI_leg = {delta_I_leg:.3f} A")

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, (ax_v, ax_i) = plt.subplots(2, 1, figsize=figsize, sharex=True)

# Current plot: CH2 and CH4 (converted from voltage, shifted left)
t_ch2 = time_us(ch["CH2"]) - CH2_SHIFT_US
t_ch4 = time_us(ch["CH4"]) - CH4_SHIFT_US
i_ch2 = ch["CH2"]["df"]["value"] * CH2_gain - CH2_offset
i_ch4 = ch["CH4"]["df"]["value"] * CH4_gain - CH4_offset

# ── Compute plot window ────────────────────────────────────────────────────────
t_data_start = max(time_us(ch["CH1"]).iloc[0], time_us(ch["CH3"]).iloc[0],
                   t_ch2.iloc[0], t_ch4.iloc[0])
t_data_end   = min(time_us(ch["CH1"]).iloc[-1], time_us(ch["CH3"]).iloc[-1],
                   t_ch2.iloc[-1], t_ch4.iloc[-1])
t_plot_start = (t_data_start + T_START_US) if T_START_US is not None else t_data_start
t_plot_end   = (t_data_start + T_END_US)   if T_END_US   is not None else \
               t_plot_start + (t_data_end - t_plot_start) / X_ZOOM

# Voltage plot: CH1 and CH3
ax_v.plot(time_us(ch["CH1"]) - t_plot_start, ch["CH1"]["df"]["value"] - VOLTAGE_OFFSET, color=color_1, linewidth=1, label=r'$v_\mathrm{1}$')
ax_v.plot(time_us(ch["CH3"]) - t_plot_start, ch["CH3"]["df"]["value"] - VOLTAGE_OFFSET, color=color_2, linewidth=1, label=r'$v_\mathrm{2}$')
ax_v.set_ylabel('[V]', rotation=0)
ax_v.yaxis.set_label_coords(-0.03, 0.92)
ax_v.legend(loc='upper right')
ax_v.grid(True, linestyle="--", alpha=0.5)

# ── Average current over one switching period ──────────────────────────────────
T_sw_us = 1 / fs * TIME_SCALE          # one period in µs
t_avg_start = t_ch2.iloc[0]
t_avg_end   = t_avg_start + T_sw_us
mask2 = (t_ch2 >= t_avg_start) & (t_ch2 <= t_avg_end)
mask4 = (t_ch4 >= t_avg_start) & (t_ch4 <= t_avg_end)
i1_avg = i_ch2[mask2].mean()
i2_avg = i_ch4[mask4].mean()
i1_pp  = i_ch2[mask2].max() - i_ch2[mask2].min()
i2_pp  = i_ch4[mask4].max() - i_ch4[mask4].min()
rec_gain_CH2 = CH2_gain * delta_I_leg / i1_pp
rec_gain_CH4 = CH4_gain * delta_I_leg / i2_pp
print(f"Expected leg current ripple ΔI_leg = {delta_I_leg:.3f} A")
print(f"Average i1 over one period: {i1_avg:.3f} A  |  Peak-to-peak: {i1_pp:.3f} A  |  Recommended CH2 gain: {rec_gain_CH2:.4f} A/V")
print(f"Average i2 over one period: {i2_avg:.3f} A  |  Peak-to-peak: {i2_pp:.3f} A  |  Recommended CH4 gain: {rec_gain_CH4:.4f} A/V")

ax_i.plot(t_ch2 - t_plot_start, i_ch2, color=color_1, linewidth=1, label=r'$i_\mathrm{1}$')
ax_i.plot(t_ch4 - t_plot_start, i_ch4, color=color_2, linewidth=1, label=r'$i_\mathrm{2}$')
ax_i.set_ylabel('[A]', rotation=0)
ax_i.yaxis.set_label_coords(-0.03, 0.92)
ax_i.legend(loc='upper right')
ax_i.grid(True, linestyle="--", alpha=0.5)

# x limits: always start at 0
ax_i.set_xlim(0, t_plot_end - t_plot_start)
if X_TICKS_US is not None:
    from matplotlib.ticker import FixedLocator
    ax_i.xaxis.set_major_locator(FixedLocator(X_TICKS_US))
elif X_TICK_SPACING_US is not None:
    from matplotlib.ticker import MultipleLocator
    ax_i.xaxis.set_major_locator(MultipleLocator(X_TICK_SPACING_US))
#ax_i.set_xlabel(f"[{TIME_UNIT}]", rotation=0)
#ax_i.xaxis.set_label_coords(0.98, -0.04)
ax_i.set_xlabel(f"Time [{TIME_UNIT}]", rotation=0)

#fig.suptitle("Oscilloscope Measurements", fontsize=13, y=1.01)
fig.tight_layout()

# Apply y-axis limits and ticks after tight_layout to prevent override
if V_YLIM is not None:
    ax_v.autoscale(enable=False, axis='y')
    ax_v.set_ylim(V_YLIM)
if V_YTICKS is not None:
    from matplotlib.ticker import FixedLocator
    ax_v.yaxis.set_major_locator(FixedLocator(V_YTICKS))
if I_YLIM is not None:
    ax_i.autoscale(enable=False, axis='y')
    ax_i.set_ylim(I_YLIM)
if I_YTICKS is not None:
    from matplotlib.ticker import FixedLocator
    ax_i.yaxis.set_major_locator(FixedLocator(I_YTICKS))

plt.savefig(f"oscilloscope_{DATA_FOLDER}.pdf", backend='pdf')

plt.show()
