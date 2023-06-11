import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

class StellarEvolutionModel(nn.Module):
    def __init__(self):
        super(StellarEvolutionModel, self).__init__()
        self.fc1 = nn.Linear(4, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 4)  # Output layer for the four variables: mass, radius, luminosity, temperature

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def stellar_evolution_model(time, initial_conditions, parameters):
    model = StellarEvolutionModel()

    # Define the loss function
    criterion = nn.MSELoss()

    # Define the optimizer
    optimizer = optim.Adam(model.parameters())

    # Prepare the training data
    num_samples = 1000
    t = torch.linspace(0, time, num_samples)
    initial_conditions = torch.tensor(initial_conditions).repeat(num_samples, 1)
    inputs = initial_conditions[:, 1:]  # Remove the time feature from the input

    # Train the model
    for epoch in range(100):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, inputs)
        loss.backward()
        optimizer.step()

    # Predict the evolution of stellar parameters
    predictions = model(inputs).detach().numpy()

    return t.numpy(), predictions[:, 0], predictions[:, 1], predictions[:, 2], predictions[:, 3]

# Example usage
initial_conditions = [1.0, 0.0, 1.0, 5000.0]
parameters = [0.5, 2.0, 1e-5]
time = 10.0
t, mass, radius, luminosity, temperature = stellar_evolution_model(time, initial_conditions, parameters)

# Plot the evolution of stellar parameters
plt.figure(figsize=(10, 8))
plt.subplot(411)
plt.plot(t, mass)
plt.xlabel('Time')
plt.ylabel('Mass')
plt.title('Stellar Evolution')

plt.subplot(412)
plt.plot(t, radius)
plt.xlabel('Time')
plt.ylabel('Radius')

plt.subplot(413)
plt.plot(t, luminosity)
plt.xlabel('Time')
plt.ylabel('Luminosity')

plt.subplot(414)
plt.plot(t, temperature)
plt.xlabel('Time')
plt.ylabel('Temperature')

plt.tight_layout()
plt.show()