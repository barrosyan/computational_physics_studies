import random
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier

# Define the paths
paths = ['Path 1', 'Path 2', 'Path 3']

# Generate synthetic data
num_samples = 1000
positions = np.random.randint(0, 10, size=num_samples)
previous_paths = np.random.choice(paths, size=num_samples)
obstacles = np.random.choice([True, False], size=num_samples)
target_labels = np.random.choice(paths, size=num_samples)

# Encode target labels
label_encoder = LabelEncoder()
target_labels_encoded = label_encoder.fit_transform(target_labels)

# One-hot encode previous_paths
ordinal_encoder = OrdinalEncoder()
previous_paths_encoded = ordinal_encoder.fit_transform(previous_paths.reshape(-1, 1)).astype(float)

# Create feature matrix X_train
X_train = np.column_stack((positions, previous_paths_encoded, obstacles))

# Create target array y_train
y_train = target_labels_encoded

# Replace missing values with NaN
X_train[X_train == 'N/A'] = np.nan

# Convert X_train to float type
X_train = X_train.astype(float)

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)

# Create and train the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Initialize the person's position and path
person_pos = 0
previous_path = None

# Simulation loop
while person_pos < 10:
    # Determine the current state (features)
    current_position = person_pos
    current_path = previous_path
    obstacle_present = random.choice([True, False])

    # Prepare the input for the model
    input_features = np.array([[current_position, current_path, obstacle_present]])

    # Replace missing values with NaN
    input_features[input_features == 'N/A'] = np.nan

    # Convert input_features to float type
    input_features = input_features.astype(float)

    # Impute missing values with the mean using the same imputer
    input_features = imputer.transform(input_features)

    # Predict the optimal path using the trained model
    predicted_label = label_encoder.inverse_transform(model.predict(input_features))[0]

    # Update the person's position and previous path
    previous_path = predicted_label
    person_pos += 1

    # Handle obstacles
    if obstacle_present:
        print(f"Obstacle found on {predicted_label}. Returning to the starting point.")
        if previous_path == paths[-1]:
            print("All paths are busy.")
            break
        else:
            continue

    # Continue simulation
    print(f"Moving to {predicted_label}...")

from manim import *

class PathSimulation(Scene):
    def construct(self):
        # Define the paths
        paths = ['Path 1', 'Path 2', 'Path 3']

        # Initialize the person's position and path
        person_pos = 0
        previous_path = None

        while person_pos < 10:
            # Determine the current state (features)
            current_position = person_pos
            current_path = previous_path
            obstacle_present = random.choice([True, False])

            # Draw the person's position
            person = Circle(radius=0.5, color=BLUE)
            person.move_to(LEFT * 5 + DOWN * person_pos)
            self.play(ShowCreation(person))

            # Draw the paths
            for i, path in enumerate(paths):
                path_line = Line(start=LEFT * 5, end=RIGHT * 5)
                path_line.move_to(DOWN * i)
                self.play(ShowCreation(path_line))

            # Draw obstacles
            if obstacle_present:
                obstacle = Star()
                obstacle.move_to(person.get_center())
                self.play(ShowCreation(obstacle))
                self.wait(1)

                # Handle obstacles
                if previous_path == paths[-1]:
                    message = Text("All paths are busy.", color=RED)
                    message.next_to(person, UP)
                    self.play(Write(message))
                    self.wait(1)
                    break
                else:
                    continue

            # Update the person's position and previous path
            previous_path = random.choice(paths)
            person_pos += 1

            # Move the person along the path
            self.play(person.animate.move_to(RIGHT * 5), run_time=1)

        self.wait(1)