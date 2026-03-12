import numpy as np

# Current probe conversion: I = V * gain - offset
CH2_offset = -68.3#-51      # A
CH2_gain   = 37.3#32       # A/V
CH4_offset = 28.63#37       # A
CH4_gain   = 24.2#23       # A/V

VOLTAGE_OFFSET = -48  # V  (subtracted from CH1 and CH3)

CH2_SHIFT_US = -10e-3  # µs — individual shift for CH2
CH4_SHIFT_US = 10e-3  # µs — individual shift for CH4

# ── Expected current ripple ────────────────────────────────────────────────────
# ΔI_leg = (Vin * Deff) / (2 * fs * Lself) * (2/(1+k) * (1/2 - Deff) + 1/(1-k))
Vin   = 48       # V
Deff  = 0.25     # -
fs    = 2e6      # Hz
Lself = 77e-9    # H
k     = -0.33    # coupling factor

X_ZOOM = 1        # zoom factor for x-axis (2 = show only half the recorded time)
T_START_US = 0.59
T_END_US = 1.59
X_TICK_SPACING_US = 0.1
X_TICKS_US = np.linspace(0, 0.9, num=10)  # e.g. [0, 0.25, 0.5]  — explicit x tick values [µs]; overrides X_TICK_SPACING_US

V_YLIM    = (-20,65)    # voltage y-axis limits; None = automatic
V_YTICKS  = [0, 48]     # voltage y-axis tick values; None = automatic

I_YLIM    = (-30,55)  # e.g. (-5, 60)      — current y-axis limits; None = automatic
I_YTICKS  = [-20, 0, 20, 40]  # e.g. [-10, 0, 10]  — current y-axis tick values; None = automatic