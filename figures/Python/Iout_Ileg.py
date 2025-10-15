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
D_values = [0.2, 0.3, 0.4]
line_styles = ['--', '-.', ':']
markers = ['o', 's', '^']

# Modern, modest colors
color_left = '#2E86AB'   # Modern blue for left axis (DeltaIout)
color_right = '#A23B72'  # Modern burgundy for right axis (DeltaIleg)

# Create figure with dual y-axes
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# Plot for each duty cycle
legend_handles = []
legend_labels = []

for i, Deff in enumerate(D_values):
    # Calculate DeltaIout
    DeltaIout = 2 / ((1 + k)) * Deff * (0.5 - Deff)
    
    # Calculate DeltaIleg
    DeltaIleg = Deff / 2 * (2 / (1 + k) * (0.5 - Deff) + 1 / (1 - k))
    
    # Plot DeltaIout on left y-axis (all in left axis color)
    line1 = ax1.plot(k, DeltaIout, 
                     linestyle=line_styles[i], 
                     color=color_left, 
                     marker=markers[i],
                     markevery=50,
                     markersize=6,
                     linewidth=2)
    
    # Plot DeltaIleg on right y-axis (all in right axis color)
    line2 = ax2.plot(k, DeltaIleg, 
                     linestyle=line_styles[i], 
                     color=color_right, 
                     marker=markers[i],
                     markevery=50,
                     markersize=6,
                     linewidth=2,
                     alpha=0.8)
    
    # Add to legend (use a black line to represent the duty cycle)
    legend_line = plt.Line2D([0], [0], color='black', linewidth=2, 
                            linestyle=line_styles[i], marker=markers[i], 
                            markersize=6)
    legend_handles.append(legend_line)
    legend_labels.append(f'D = {Deff}')

# Set labels and formatting with matching colors
ax1.set_xlabel('k', fontsize=12, color='#333333')
ax1.set_ylabel('ΔIout (A)', fontsize=12, color=color_left, fontweight='bold')
ax2.set_ylabel('ΔIleg (A)', fontsize=12, color=color_right, fontweight='bold')

# Color the y-axis ticks to match
ax1.tick_params(axis='y', colors=color_left)
ax2.tick_params(axis='y', colors=color_right)

# Set x-axis limits
ax1.set_xlim(-kmax, kmax)

# Add grid
ax1.grid(True, alpha=0.3, color='#CCCCCC')

# Create single legend with black color showing duty cycles
legend = ax1.legend(legend_handles, legend_labels, loc='upper left', fontsize=10,
                   framealpha=0.9, fancybox=True, edgecolor='black')
# Set legend text color to black
for text in legend.get_texts():
    text.set_color('black')

# Add title
plt.title('Current Ripple vs Coupling Factor k\n' + 
          f'Vin={Vin}V, fs={fs/1000:.0f}kHz, Lself={Lself*1e6:.0f}μH', 
          fontsize=14, color='#333333', pad=20)

# Set spine colors to be subtle
ax1.spines['left'].set_color(color_left)
ax1.spines['left'].set_linewidth(2)
ax2.spines['right'].set_color(color_right)
ax2.spines['right'].set_linewidth(2)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_color('#666666')

# Tight layout and show
plt.tight_layout()
plt.show()

# Print parameter values used
print(f"Parameters used:")
print(f"Vin = {Vin} V")
print(f"fs = {fs/1000:.0f} kHz") 
print(f"Lself = {Lself*1e6:.0f} μH")
print(f"Duty cycles: {D_values}")
print(f"Colors: Left axis (ΔIout) = {color_left}, Right axis (ΔIleg) = {color_right}")