import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^−1 s^−2)
c = 2.998e8  # Speed of light (m/s)
sigma = 5.670374419e-8  # Stefan-Boltzmann constant (W m^−2 K^−4)
mu = 0.62  # Mean molecular weight for solar composition
kappa_es = 0.02  # Electron scattering opacity (cm^2/g)
kappa_ff = 1.0e24  # Free-free absorption opacity (cm^2/g)

# Stellar evolution simulation function
def simulate_stellar_evolution(initial_mass, initial_radius, initial_temperature, simulation_time, time_step):
    # Initialize arrays to store evolution data
    time = np.arange(0, simulation_time, time_step)
    mass = np.zeros_like(time)
    radius = np.zeros_like(time)
    luminosity = np.zeros_like(time)
    temperature = np.zeros_like(time)

    # Set initial values
    mass[0] = initial_mass
    radius[0] = initial_radius
    temperature[0] = initial_temperature

    # Simulation loop
    for i in range(1, len(time)):
        # Calculate luminosity
        luminosity[i] = 4 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**4

        # Calculate rate of change of mass
        dm_dt = -luminosity[i] / (c**2)

        # Calculate rate of change of radius
        dr_dt = -(3 * luminosity[i] * kappa(i, temperature[i-1])) / (16 * np.pi * G * c * radius[i-1]**2 * temperature[i-1]**3)

        # Calculate rate of change of temperature
        dT_dt = -3 * G * mass[i-1] * dm_dt * (1 - (1 / gamma(i, temperature[i-1]))) / (16 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**3)

        # Update variables
        mass[i] = mass[i-1] + dm_dt * time_step
        radius[i] = radius[i-1] + dr_dt * time_step
        temperature[i] = temperature[i-1] + dT_dt * time_step

    return time, mass, radius, luminosity, temperature

# Function to calculate opacity
def kappa(i, T):
    # Combine electron scattering and free-free absorption
    return (1 / kappa_es + 1 / kappa_ff) * (1 + gamma(i, T))

# Function to calculate adiabatic exponent
def gamma(i, T):
    # Use polytropic relation for simplicity
    return (4 / 3) - (4 / 3) * (T / (10**6))**(2 / 3)

# Initial conditions
initial_mass = 1.0  # Initial stellar mass in solar masses
initial_radius = 1.0  # Initial stellar radius in solar radii
initial_temperature = 5778  # Initial stellar temperature in Kelvin

# Simulation parameters
simulation_time = 10e6  # Total simulation time in years
time_step = 1000  # Time step in years

# Run the simulation
time, mass, radius, luminosity, temperature = simulate_stellar_evolution(initial_mass, initial_radius, initial_temperature, simulation_time, time_step)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(time, mass, label='Mass')
plt.plot(time, radius, label='Radius')
plt.plot(time, luminosity, label='Luminosity')
plt.plot(time, temperature, label='Temperature')
plt.xlabel('Time (years)')
plt.ylabel('Value')
plt.title('Stellar Evolution Simulation')
plt.legend()
plt.grid(True)
plt.show()

# Neural network model for stellar evolution
def create_stellar_evolution_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(3,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Function to calculate opacity
def kappa(T, rho):
    return (1 / kappa_es + 1 / kappa_ff) * (1 + gamma(T, rho))

# Function to calculate adiabatic exponent
def gamma(T, rho):
    return (4 / 3) - (4 / 3) * (T / (10**6))**(2 / 3)

# Stellar evolution simulation function using neural network model
def simulate_stellar_evolution_nn(initial_mass, initial_radius, initial_temperature, simulation_time, time_step):
    # Initialize arrays to store evolution data
    time = np.arange(0, simulation_time, time_step)
    mass = np.zeros_like(time)
    radius = np.zeros_like(time)
    luminosity = np.zeros_like(time)
    temperature = np.zeros_like(time)

    # Set initial values
    mass[0] = initial_mass
    radius[0] = initial_radius
    temperature[0] = initial_temperature

    # Neural network model
    model = create_stellar_evolution_model()

    # Convert variables to tensors
    inputs = np.zeros((1, 3))
    inputs[0] = [0, radius[0], temperature[0]]

    # Simulation loop
    for i in range(1, len(time)):
        # Calculate luminosity
        luminosity[i] = 4 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**4

        # Calculate rate of change of mass
        dm_dt = -luminosity[i] / (c**2)

        # Calculate rate of change of radius
        dr_dt = -(3 * luminosity[i] * kappa(temperature[i-1], 0)) / (16 * np.pi * G * c * radius[i-1]**2 * temperature[i-1]**3)

        # Calculate rate of change of temperature
        dT_dt = -3 * G * mass[i-1] * dm_dt * (1 - (1 / gamma(temperature[i-1], 0))) / (16 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**3)

        # Update variables using neural network model
        inputs[0, 0] = dm_dt
        inputs[0, 1] = radius[i-1]
        inputs[0, 2] = temperature[i-1]
        dm_dt_pred = model.predict(inputs)
        mass[i] = mass[i-1] + dm_dt_pred[0, 0]
        radius[i] = radius[i-1] + dr_dt
        temperature[i] = temperature[i-1] + dT_dt

        # Prepare inputs for the next iteration
        inputs[0, 0] = dm_dt_pred[0, 0]

        # Prepare targets for training
        targets = np.array([[dm_dt]])

        # Convert inputs and targets to tensors
        inputs_tensor = tf.convert_to_tensor(inputs, dtype=tf.float32)
        targets_tensor = tf.convert_to_tensor(targets, dtype=tf.float32)

        # Train the neural network model and get the loss
        loss = model.train_on_batch(inputs_tensor, targets_tensor)

        # Calculate and print the training step accuracy
        accuracy = 1 - loss
        print(f"Training Step: {i}, Accuracy: {accuracy}")

    return time, mass, radius, luminosity, temperature

# Run the physics-based simulation
time, mass_physics, radius_physics, luminosity_physics, temperature_physics = simulate_stellar_evolution(initial_mass, initial_radius, initial_temperature, simulation_time, time_step)

# Run the neural network-based simulation
time, mass_nn, radius_nn, luminosity_nn, temperature_nn = simulate_stellar_evolution_nn(initial_mass, initial_radius, initial_temperature, simulation_time, time_step)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(time, mass_physics, label='Physics-based (Mass)')
plt.plot(time, mass_nn, label='Neural Network-based (Mass)')
plt.plot(time, radius_physics, label='Physics-based (Radius)')
plt.plot(time, radius_nn, label='Neural Network-based (Radius)')
plt.plot(time, luminosity_physics, label='Physics-based (Luminosity)')
plt.plot(time, luminosity_nn, label='Neural Network-based (Luminosity)')
plt.plot(time, temperature_physics, label='Physics-based (Temperature)')
plt.plot(time, temperature_nn, label='Neural Network-based (Temperature)')
plt.xlabel('Time (years)')
plt.ylabel('Value')
plt.title('Stellar Evolution Comparison')
plt.legend()
plt.grid(True)
plt.show()# Constants

G = 6.67430e-11  # Gravitational constant (m^3 kg^−1 s^−2)
c = 2.998e8  # Speed of light (m/s)
sigma = 5.670374419e-8  # Stefan-Boltzmann constant (W m^−2 K^−4)
mu = 0.62  # Mean molecular weight for solar composition
kappa_es = 0.02  # Electron scattering opacity (cm^2/g)
kappa_ff = 1.0e24  # Free-free absorption opacity (cm^2/g)

# Stellar evolution simulation function
def simulate_stellar_evolution(initial_mass, initial_radius, initial_temperature, simulation_time, time_step):
    # Initialize arrays to store evolution data
    time = np.arange(0, simulation_time, time_step)
    mass = np.zeros_like(time)
    radius = np.zeros_like(time)
    luminosity = np.zeros_like(time)
    temperature = np.zeros_like(time)

    # Set initial values
    mass[0] = initial_mass
    radius[0] = initial_radius
    temperature[0] = initial_temperature

    # Simulation loop
    for i in range(1, len(time)):
        # Calculate luminosity
        luminosity[i] = 4 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**4

        # Calculate rate of change of mass
        dm_dt = -luminosity[i] / (c**2)

        # Calculate rate of change of radius
        dr_dt = -(3 * luminosity[i] * kappa(i, temperature[i-1])) / (16 * np.pi * G * c * radius[i-1]**2 * temperature[i-1]**3)

        # Calculate rate of change of temperature
        dT_dt = -3 * G * mass[i-1] * dm_dt * (1 - (1 / gamma(i, temperature[i-1]))) / (16 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**3)

        # Update variables
        mass[i] = mass[i-1] + dm_dt * time_step
        radius[i] = radius[i-1] + dr_dt * time_step
        temperature[i] = temperature[i-1] + dT_dt * time_step

    return time, mass, radius, luminosity, temperature

# Function to calculate opacity
def kappa(i, T):
    # Combine electron scattering and free-free absorption
    return (1 / kappa_es + 1 / kappa_ff) * (1 + gamma(i, T))

# Function to calculate adiabatic exponent
def gamma(i, T):
    # Use polytropic relation for simplicity
    return (4 / 3) - (4 / 3) * (T / (10**6))**(2 / 3)

# Initial conditions
initial_mass = 1.0  # Initial stellar mass in solar masses
initial_radius = 1.0  # Initial stellar radius in solar radii
initial_temperature = 5778  # Initial stellar temperature in Kelvin

# Simulation parameters
simulation_time = 10e6  # Total simulation time in years
time_step = 1000  # Time step in years

# Run the physics-based simulation
time, mass_physics, radius_physics, luminosity_physics, temperature_physics = simulate_stellar_evolution(initial_mass, initial_radius, initial_temperature, simulation_time, time_step)

# Neural network model for stellar evolution
def create_stellar_evolution_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(3,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Stellar evolution simulation function using neural network model
def simulate_stellar_evolution_nn(initial_mass, initial_radius, initial_temperature, simulation_time, time_step):
    # Initialize arrays to store evolution data
    time = np.arange(0, simulation_time, time_step)
    mass = np.zeros_like(time)
    radius = np.zeros_like(time)
    luminosity = np.zeros_like(time)
    temperature = np.zeros_like(time)

    # Set initial values
    mass[0] = initial_mass
    radius[0] = initial_radius
    temperature[0] = initial_temperature

    # Neural network model
    model = create_stellar_evolution_model()

    # Convert variables to tensors
    inputs = np.zeros((1, 3))
    inputs[0] = [0, radius[0], temperature[0]]

    # Simulation loop
    for i in range(1, len(time)):
        # Calculate luminosity
        luminosity[i] = 4 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**4

        # Calculate rate of change of mass
        dm_dt = -luminosity[i] / (c**2)

        # Calculate rate of change of radius
        dr_dt = -(3 * luminosity[i] * kappa(temperature[i-1], 0)) / (16 * np.pi * G * c * radius[i-1]**2 * temperature[i-1]**3)

        # Calculate rate of change of temperature
        dT_dt = -3 * G * mass[i-1] * dm_dt * (1 - (1 / gamma(temperature[i-1], 0))) / (16 * np.pi * radius[i-1]**2 * sigma * temperature[i-1]**3)

        # Update variables using neural network model
        inputs[0, 0] = dm_dt
        inputs[0, 1] = radius[i-1]
        inputs[0, 2] = temperature[i-1]
        dm_dt_pred = model.predict(inputs)
        mass[i] = mass[i-1] + dm_dt_pred[0, 0]
        radius[i] = radius[i-1] + dr_dt
        temperature[i] = temperature[i-1] + dT_dt

        # Prepare inputs for the next iteration
        inputs[0, 0] = dm_dt_pred[0, 0]

        # Prepare targets for training
        targets = np.array([[dm_dt]])

        # Convert inputs and targets to tensors
        inputs_tensor = tf.convert_to_tensor(inputs, dtype=tf.float32)
        targets_tensor = tf.convert_to_tensor(targets, dtype=tf.float32)

        # Train the neural network model and get the loss
        loss = model.train_on_batch(inputs_tensor, targets_tensor)

        # Calculate and print the training step accuracy
        accuracy = 1 - loss
        if accuracy<0:
            accuracy=0.0
        print(f"Training Step: {i}, Accuracy: {accuracy}")

    return time, mass, radius, luminosity, temperature

# Run the neural network-based simulation
time, mass_nn, radius_nn, luminosity_nn, temperature_nn = simulate_stellar_evolution_nn(initial_mass, initial_radius, initial_temperature, simulation_time, time_step)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(time, mass_physics, label='Physics-based (Mass)')
plt.plot(time, mass_nn, label='Neural Network-based (Mass)')
plt.plot(time, radius_physics, label='Physics-based (Radius)')
plt.plot(time, radius_nn, label='Neural Network-based (Radius)')
plt.plot(time, luminosity_physics, label='Physics-based (Luminosity)')
plt.plot(time, luminosity_nn, label='Neural Network-based (Luminosity)')
plt.plot(time, temperature_physics, label='Physics-based (Temperature)')
plt.plot(time, temperature_nn, label='Neural Network-based (Temperature)')
plt.xlabel('Time (years)')
plt.ylabel('Value')
plt.title('Stellar Evolution Comparison')
plt.legend()
plt.grid(True)
plt.show()