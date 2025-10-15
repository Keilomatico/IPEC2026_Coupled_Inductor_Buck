import numpy as np
import matplotlib.pyplot as plt

# Define k range
kmax = 0.6
k = np.linspace(-kmax, kmax, 1000)

# Define duty cycles
D_values = [0.15, 0.25, 0.35]
line_styles = ['--', '-.', ':']
markers = ['s', '^', 'o']

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
    DeltaIout = 2 / (1 + k) * Deff * (0.5 - Deff)
    
    # Calculate DeltaIleg
    DeltaIleg = Deff / 2 * (
        2 / (1 + k) * (0.5 - Deff) + 1 / (1 - k)
    )
    
    # Adjust marker positions for D=0.35 (index 2) to make them visible
    if i == 2:  # D=0.35 case
        markevery_iout = 25  # Twice as many markers
    else:
        markevery_iout = 50
    
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
            markevery=50,
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
DeltaIout_marker = 2 / (1 + k_iout) * Deff_iout * (0.5 - Deff_iout)

# Position for ΔIleg label
k_ileg = -0.3
Deff_ileg = 0.25  # Use middle duty cycle for reference
DeltaIleg_marker = Deff_ileg / 2 * (
    2 / (1 + k_ileg) * (0.5 - Deff_ileg) + 1 / (1 - k_ileg)
)

# Add ΔIout identification label (text only)
ax.annotate(r'$\Delta I_\mathrm{out}$', xy=(k_iout, DeltaIout_marker), 
            xytext=(15, 10), textcoords='offset points',
            fontsize=15, fontweight='bold', color=color_left,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor=color_left, alpha=0.9))

# Add ΔIleg identification label (text only)
ax.annotate(r'$\Delta I_\mathrm{leg}$', xy=(k_ileg, DeltaIleg_marker), 
            xytext=(15, 10), textcoords='offset points',
            fontsize=15, fontweight='bold', color=color_right,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor=color_right, alpha=0.9))

# Set labels and formatting
ax.set_xlabel('k', fontsize=12, color='#333333')
#ax.set_ylabel('Current Ripple / (Vin/(fs*L_self)', fontsize=12, color='#333333', fontweight='bold')
ax.set_ylabel(r'$\mathrm{Current~Ripple}~/~\frac{V_\mathrm{in}}{f_\mathrm{s} L_\mathrm{self}}$', fontsize=12, color='#333333', fontweight='bold')
#ax.set_ylabel(r'Current Ripple / ($V_\mathrm{in}$/($f_\mathrm{s}$ $L_\mathrm{self}$))', fontsize=12, color='#333333', fontweight='bold')

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

# Clean up spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#666666')
ax.spines['bottom'].set_color('#666666')

# Tight layout and show
plt.tight_layout()
plt.show()