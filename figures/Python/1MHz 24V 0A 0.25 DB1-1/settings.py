# Current probe conversion: I = V * gain - offset
CH2_offset = -51      # A
CH2_gain   = 32       # A/V
CH4_offset = 37       # A
CH4_gain   = 23       # A/V

VOLTAGE_OFFSET = -24  # V  (subtracted from CH1 and CH3)

CURRENT_SHIFT_US = 30e-3  # µs  (30 ns → shift current channels left)

# ── Expected current ripple ────────────────────────────────────────────────────
# ΔI_leg = (Vin * Deff) / (2 * fs * Lself) * (2/(1+k) * (1/2 - Deff) + 1/(1-k))
Vin   = 24       # V
Deff  = 0.25     # -
fs    = 1e6      # Hz
Lself = 77e-9    # H
k     = -0.33    # coupling factor

X_ZOOM = 1        # zoom factor for x-axis (2 = show only half the recorded time)

T_START_US = None  # µs — start of plot window; None or 0 = first sample
T_END_US   = None  # µs — end of plot window;   None = last sample (respects X_ZOOM)

X_TICK_SPACING_US = None  # µs — spacing between x ticks; None = automatic

V_YLIM    = None  # e.g. (-5, 60)      — voltage y-axis limits; None = automatic
V_YTICKS  = None  # e.g. [0, 20, 40]   — voltage y-axis tick values; None = automatic

I_YLIM    = None  # e.g. (-5, 60)      — current y-axis limits; None = automatic
I_YTICKS  = None  # e.g. [-10, 0, 10]  — current y-axis tick values; None = automatic
