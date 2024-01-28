import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit

# Define the Lotka-Volterra model

def lotka_volterra_extended(predator_prey, t, a, b, c, d, r, k):
    H, L = predator_prey
    dHdt = r*H*(1 - H/k) - (a*H*L)/(c + H)
    dLdt = (b*H*L)/(c + H) - d*L
    return [dHdt, dLdt]

# Function to integrate Lotka-Volterra model for curve_fit
def fit_lotka_volterra(t, a, b, c, d, r, k):
    starting_populations = [30, 4]  # Example starting values
    solution = odeint(lotka_volterra_extended, starting_populations, t, args=(a, b, c, d, r, k))
    return solution.ravel()

# Actual data
time_points = np.linspace(0, 20, 21)  # Replace with actual time points
hare_data = np.array([30,47.2,70.2,77.4,36.3,20.6,18.1,21.4,22,25.4,27.1,40.3,57,76.6,52.3,19.5,11.2,7.6,14.6,16.2,24.7]) 
lynx_data = np.array([4,6.1,9.8,35.2,59.4,41.7,19,13,8.3,9.1,7.4,8,12.33,19.5,45.7,51.1,29.7,15.8,9.7,10.1,8.6]) 


actual_data = np.vstack((hare_data, lynx_data)).ravel()  # Stack the data for curve_fit

# Initial guess for parameters
initial_guess = [0.5, 0.4, 0.3, 0.09, 0.2, 400]

# Use curve_fit to find the best parameters
optimal_params, covariance = curve_fit(fit_lotka_volterra, time_points, actual_data, p0=initial_guess)

# Optimal parameters to solve the Lotka-Volterra model
t = np.linspace(0, 30, 100)
solution = odeint(lotka_volterra_extended, [30, 4], t, args=tuple(optimal_params))

# Plotting the results
plt.figure(figsize=(12, 5))

# First subplot
plt.subplot(1, 2, 1)
plt.plot(t, solution[:, 0], label='Prey (Model)')
plt.plot(t, solution[:, 1], label='Predator (Model)')
plt.scatter(time_points, hare_data, color='blue', label='Prey (Data)')
plt.scatter(time_points, lynx_data, color='red', label='Predator (Data)')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()

# Phase plot
t = np.linspace(0, 70, 500)  # Time grid
IC = [30, 4]  # Initial conditions for H and L
sol = odeint(lotka_volterra_extended, IC, t, args=tuple(optimal_params))  # Compute solution
H, L = sol.transpose()  # Unpack solution

# Second subplot
plt.subplot(1, 2, 2)
plt.plot(H, L)
plt.title('Hare/Lynx Phase Plot')
plt.xlabel('Hare')
plt.ylabel('Lynx')
plt.grid(True)

plt.tight_layout()
plt.show()

print("Optimal Parameters:", optimal_params)
