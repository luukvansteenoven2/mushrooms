import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def lotka_volterra(predator_prey, t, a, b, c, d):
    x, y = predator_prey
    dxdt = a * x - b * x * y
    dydt = c * x * y - d * y
    return [dxdt, dydt]

parameter_sets = [
    (1.0, 0.1, 0.1, 1.0),  # Balanced growth and predation rates 
    (0.5, 0.1, 0.1, 1.0),  # Reduced prey growth rates
    (1.5,0.1,0.1,1.0), #Increased prey growth rates
    (1.0, 0.05, 0.1, 1.0), #Reduced predation rate 
    (1.0, 0.2, 0.1, 1.0), #Increased predation rate
    (1.0, 0.1, 0.05, 1.0), #Reduced predator efficiency 
    (1.0,0.1,0.2,1.0), #Increased predator efficiency
    (1.0, 0.1, 0.1, 0.5), #Reduced predator mortality rate
    (1.0, 0.1, 0.1, 1.5) #Increased predator mortality rate:
]

for params in parameter_sets:
    t = np.linspace(0, 30, 100)
    solution = odeint(lotka_volterra, [30, 4], t, args=params)
    
    plt.plot(t, solution[:, 0], label='Prey')
    plt.plot(t, solution[:, 1], label='Predator')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.show()
