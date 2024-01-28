import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def lotka_volterra_extended(predator_prey, t, a, b, c, d, r, k):
    H, L = predator_prey
    dHdt = r*H*(1 - H/k) - (a*H*L)/(c + H)
    dLdt = (b*H*L)/(c + H) - d*L
    return [dHdt, dLdt]

parameter_sets = [
    #these parameters are wrong
    #a=prey growth rate 
    #b=prediation rate (rate at which predator consume prey)
    #c=conversion efficiency (predator birthing rate)
    #d=predator mortatliy rate 
    #r = growth rate again for prey 
    #k= carry cap
    (0.4, 0.4, 0.6, 0.001, 0.6, 2000),
    (0.5, 0.4, 0.3, 0.09, 0.2, 400),
    (0.3, 4/3, 0.03, 0.2, 0.09, 300),
    (1.2, 0.8, 0.05, 0.0001,0.9,250)
]

for params in parameter_sets:
    t = np.linspace(0, 30, 100)
    solution = odeint(lotka_volterra_extended, [200, 4], t, args=params) 
    #in the part where it says 30 and 4 this is the initial population 
    
    plt.plot(t, solution[:, 0], label='Prey')
    plt.plot(t, solution[:, 1], label='Predator')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.show()
