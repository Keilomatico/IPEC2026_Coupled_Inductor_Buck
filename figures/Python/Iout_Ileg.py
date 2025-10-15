import numpy as np
import matplotlib.pyplot as plt

# Define constants (you can adjust these values as needed)
Vin = 12  # Input voltage (V)
fs = 100e3  # Switching frequency (Hz)
Lself = 10e-6  # Self inductance (H)

# Define k range
kmax = 0.6
k = np.linspace(-kmax, kmax, 1000)

# Define duty cycles
D_values = [0.15, 0.25, 0.35]
line_styles = ['--', '-.', ':']
markers = ['o', 's', '^']

# Modern, modest colors
color_left = '#2E86AB'   # Modern blue for DeltaIout
color_right = '#A23B72'  # Modern burgundy for DeltaIleg

# Create figure with single y-axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot for each duty cycle
legend_handles = []
legend_labels = []

for i, Deff in enumerate(D_values):
    # Calculate DeltaIout
    DeltaIout = (2 * Vin) / (fs * (1 + k) * Lself) * Deff * (0.5 - Deff)
    
    # Calculate DeltaIleg
    DeltaIleg = (Vin * Deff) / (2 * fs * Lself) * (
        2 / (1 + k) * (0.5 - Deff) + 1 / (1 - k)
    )
    
    # Adjust marker positions for D=0.3 (index 2) to make them visible
    if i == 2:  # D=0.3 case
        markevery_iout = 25  # Slightly offset from the standard 50
        markevery_ileg = 50
    else:
        markevery_iout = 50
        markevery_ileg = 50
    
    # Plot DeltaIout
    ax.plot(k, DeltaIout, 
            linestyle=line_styles[i], 
            color=color_left, 
            marker=markers[i],
            markevery=markevery_iout,
            markersize=6,
            linewidth=2)
    
    # Plot DeltaIleg
    ax.plot(k, DeltaIleg, 
            linestyle=line_styles[i], 
            color=color_right, 
            marker=markers[i],
            markevery=markevery_ileg,
            markersize=6,
            linewidth=2,
            alpha=0.8)
    
    # Add to legend with longer lines
    legend_line = plt.Line2D([0], [0], color='black', linewidth=2, 
                            linestyle=line_styles[i], marker=markers[i], 
                            markersize=6)
    legend_handles.append(legend_line)
    legend_labels.append(f'D = {Deff}')

# Add identification labels (no markers, just text)
# Position for ΔIout label
k_iout = 0.0
Deff_iout = 0.25  # Use middle duty cycle for positioning
DeltaIout_marker = (2 * Vin) / (fs * (1 + k_iout) * Lself) * Deff_iout * (0.5 - Deff_iout)

# Position for ΔIleg label
k_ileg = -0.3
Deff_ileg = 0.25  # Use middle duty cycle for reference
DeltaIleg_marker = (Vin * Deff_ileg) / (2 * fs * Lself) * (
    2 / (1 + k_ileg) * (0.5 - Deff_ileg) + 1 / (1 - k_ileg)
)

# Add ΔIout identification label (text only)
ax.annotate('ΔIout', xy=(k_iout, DeltaIout_marker), 
            xytext=(15, 10), textcoords='offset points',
            fontsize=15, fontweight='bold', color=color_left,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor=color_left, alpha=0.9))

# Add ΔIleg identification label (text only)
ax.annotate('ΔIleg', xy=(k_ileg, DeltaIleg_marker), 
            xytext=(15, 10), textcoords='offset points',
            fontsize=15, fontweight='bold', color=color_right,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor=color_right, alpha=0.9))

# Set labels and formatting
ax.set_xlabel('k', fontsize=12, color='#333333')
ax.set_ylabel('Current Ripple (A)', fontsize=12, color='#333333', fontweight='bold')

# Set x-axis limits
ax.set_xlim(-kmax, kmax)

# Add grid
ax.grid(True, alpha=0.3, color='#CCCCCC')

# Create single legend with black color showing duty cycles
legend = ax.legend(legend_handles, legend_labels, loc='upper left', fontsize=10,
                  framealpha=0.9, fancybox=True, edgecolor='black')
# Set legend text color to black
for text in legend.get_texts():
    text.set_color('black')

# Add title
plt.title('Current Ripple vs Coupling Factor k\n' + 
          f'Vin={Vin}V, fs={fs/1000:.0f}kHz, Lself={Lself*1e6:.0f}μH', 
          fontsize=14, color='#333333', pad=20)

# Clean up spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#666666')
ax.spines['bottom'].set_color('#666666')

# Tight layout and show
plt.tight_layout()
plt.show()

# Print parameter values used
print(f"Parameters used:")
print(f"Vin = {Vin} V")
print(f"fs = {fs/1000:.0f} kHz") 
print(f"Lself = {Lself*1e6:.0f} μH")
print(f"Duty cycles: {D_values}")
print(f"k range: -{kmax} to {kmax}")
print(f"Colors: ΔIout = {color_left}, ΔIleg = {color_right}")