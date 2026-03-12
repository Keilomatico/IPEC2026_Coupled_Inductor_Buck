# Current probe conversion: I = V * gain - offset
CH2_offset = -61.5#-51      # A
CH2_gain   = 37.3#32       # A/V
CH4_offset = 40.4#37       # A
CH4_gain   = 24.2#23       # A/V
VOLTAGE_OFFSET = -48  # V  (subtracted from CH1 and CH3)
CURRENT_SHIFT_US = 0e-3  # µs  (30 ns → shift current channels left)


# ── Expected current ripple ────────────────────────────────────────────────────
# ΔI_leg = (Vin * Deff) / (2 * fs * Lself) * (2/(1+k) * (1/2 - Deff) + 1/(1-k))
Vin   = 48       # V
Deff  = 0.25     # -
fs    = 2e6      # Hz
Lself = 77e-9    # H
k     = -0.33    # coupling factor

# Plotting
X_ZOOM = 1        # zoom factor for x-axis (2 = show only half the recorded time)
T_START_US = 0.35
T_END_US = 1.35
X_TICK_SPACING_US = 0.1

V_YLIM    = (0,15)
V_YTICKS  = [0, 48]  # e.g. [0, 20, 40]   — voltage y-axis tick values; None = automatic
I_YLIM    = None  # e.g. (-5, 60)      — current y-axis limits; None = automatic
I_YTICKS  = None  # e.g. [-10, 0, 10]  — current y-axis tick values; None = automatic

