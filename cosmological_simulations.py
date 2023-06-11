import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MultipleLocator

def cosmological_simulation(parameters):
    # Extract simulation parameters
    initial_conditions = parameters['initial_conditions']
    model_parameters = parameters['model_parameters']
    simulation_time = parameters['simulation_time']

    # Extract model parameters
    H0 = model_parameters['H0']  # Hubble constant
    Omega_m = model_parameters['Omega_m']  # Matter density parameter

    # Define the time grid
    time = np.linspace(0, simulation_time, num=100)

    # Initialize arrays for storing simulation results
    a = np.zeros_like(time)  # Scale factor
    t = np.zeros_like(time)  # Cosmic time

    # Set initial conditions
    a[0] = initial_conditions[0]
    t[0] = initial_conditions[1]

    # Perform simulation
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        da = H0 * a[i-1] * np.sqrt(Omega_m / a[i-1]**3) * dt
        a[i] = a[i-1] + da
        t[i] = t[i-1] + dt

    return t, a

# Example usage
simulation_parameters = {
    'initial_conditions': [1.0, 0.0],  # Initial scale factor and cosmic time
    'model_parameters': {
        'H0': 70,  # Hubble constant in km/s/Mpc
        'Omega_m': 0.3  # Matter density parameter
    },
    'simulation_time': 10.0  # Time span of the simulation
}
t, a = cosmological_simulation(simulation_parameters)

# Create a modern and beautiful visualization
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(14, 8))
figManager = plt.get_current_fig_manager()
figManager.full_screen_toggle()
fig.suptitle('Cosmological Simulation Dashboard', color='white', fontsize=16)

# Set the background color of ax1 to transparent
ax1.patch.set_alpha(0)

# Plot the scale factor with custom styling
ax1.plot(t, a, color='red', linewidth=2)
ax1.set_xlabel('Cosmic Time', color='white', fontsize=10)
ax1.set_ylabel('Scale Factor', color='white', fontsize=10)
ax1.set_title('Scale Factor Evolution', color='white', fontsize=12)
ax1.xaxis.set_major_locator(MultipleLocator(1.0))  # Show major ticks every 1 unit on x-axis

# Animate the scale factor
line, = ax2.plot([], [], marker='o', color='white')

def update(frame):
    ax1.lines[0].set_data(t[:frame], a[:frame])  # Update data of ax1
    line.set_data(t[:frame], a[:frame])  # Update data of ax2
    return ax1.lines[0], line

ani = FuncAnimation(fig, update, frames=len(t), blit=True)

# Remove the legend from the plot
if ax1.get_legend():
    ax1.get_legend().remove()

# Remove x and y axis from ax2
ax2.axis('off')

# Adjust the legend box size to match the plot
legend_bbox = ax2.get_position()
legend_height = legend_bbox.height

# Create a combined text with simulation parameters, explanations, and suggestions
combined_text = f"------ Simulation Parameters: ------\n\n\n"
combined_text += f"1. Initial Conditions:\n\n"
combined_text += f"  Scale Factor: {simulation_parameters['initial_conditions'][0]}\n\n"
combined_text += f"  Cosmic Time: {simulation_parameters['initial_conditions'][1]}\n\n\n"
combined_text += f"2. Model Parameters:\n\n"
combined_text += f"  Hubble Constant: {simulation_parameters['model_parameters']['H0']} km/s/Mpc\n\n"
combined_text += f"  Matter Density Parameter: {simulation_parameters['model_parameters']['Omega_m']}\n\n\n"
combined_text += f"3. Simulation Time: {simulation_parameters['simulation_time']}\n\n\n"
combined_text += "4. Explanations:\n\n"
combined_text += "  Scale Factor: A measure of the expansion of the universe\n\n"
combined_text += "  Cosmic Time: The age of the universe since the Big Bang\n\n\n"
combined_text += "5. Suggestions:\n\n"
combined_text += "  The graphic suggests the evolution of the scale factor\n\nwith respect to cosmic time."

# Set the position and style of the combined text box
ax2.text(0, 0.5, combined_text, fontsize=9, verticalalignment='center', transform=ax2.transAxes,
         wrap=True)

# Set the font color for suggestions and explanations
texts = ax2.texts
if len(texts) >= 2:
    texts[0].set_color('blue')  # Suggestions
    texts[1].set_color('red')  # Explanations

# Set the length of the second plot to match the first plot
ax2.set_xlim(0, len(t)*10)

# Set layout and display the dashboard
plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.show()
