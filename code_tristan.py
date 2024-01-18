# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:19:04 2024

@author: trist
"""

print("I am Tristan I like mushrooms too")

import matplotlib.pyplot as plt
import numpy as np

seed = 160

def randint(a=1664525, c=1013904223, m=2**32):
    global seed
    seed = (a * seed + c) % m
    return seed

def rand():
    r_int = randint()
    return r_int/(2**32)

def drawing_with_replacement(data,n=10**2):
    new_sample = list(range(n))
    for i in range(n):
        new_sample[i] = data[int(rand()*len(data))]
    return new_sample

class Model:
    def __init__(self, width=50, height=50, nPredator=100, nPrey=500,
                 initPredatorHungry=0.5, biteProb=0.8):
        """
        Model parameters
        Initialize the model with the width and height parameters.
        """
        self.height = height
        self.width = width
        self.nPredator = nPredator
        self.nPrey = nPrey
        self.biteProb = biteProb
        self.PredatorHungry = initPredatorHungry ## Percentage of predators that are hungry from start
        self.list_indexes_not_had = []
        self.mortality_rate = 0.001
        
        # We make a list with all possible grid positions
        for i in range(self.width):
            for j in range(self.height):
                self.list_indexes_not_had.append([i,j])
        
        self.time_alive = [0] * nPrey
        

        """
        Data parameters
        To record the evolution of the model
        """
        self.bornPreyCount = 0
        self.deathPreyCount = 0
        self.bornPredatorCount = 0
        self.deathPredatorCount = 0

        """
        Population setters
        Make a data structure in this case a list with the Predators and Preys.
        """
        self.PredatorPopulation = self.set_predator_population(nPredator)
        self.PreyPopulation = self.set_prey_population(nPrey)

    def set_prey_population(self):
        """
        This function makes the initial Prey population, by iteratively adding
        an object of the Prey class to the PreyPopulation list.
        The position of each Prey object is randomized. 
        """
        
        PreyPopulation = []
        for i in range(self.nPrey):
            """
            Preys may not have overlapping positions.
            """
            # When we generate a new Prey, we get their position and we take their current position out of our grid list
            x_y = drawing_with_replacement(self.list_indexes_not_had,1)
            x = x_y[0][0]
            y = x_y[0][1]
            self.list_indexes_not_had.remove(x_y[0])   
            state = 'A'  # A for alive
                 
            # We add the Predator we 'created' to our population
            PreyPopulation.append(Prey(x, y, state))
        return PreyPopulation


    def set_predator_population(self, initPredatorHungry):
        """
        This function makes the initial Predator population, by iteratively
        adding an object of the Predator class to the PredatorPopulation list.
        The position of each Predator object is randomized.
        A number of Predator objects is initialized with the "hungry" state.
        """
        PredatorPopulation = []
        for i in range(self.nPredator):
            # When we generate a new Predator, we get their position and we take their current position out of our grid list
            x_y = drawing_with_replacement(self.list_indexes_not_had,1)
            x = x_y[0][0]
            y = x_y[0][1]
            self.list_indexes_not_had.remove(x_y[0])  
            if (i / self.nPredator) <= initPredatorHungry: # See wether the Predator is hungry or not 
                hungry = True
            else:
                hungry = False
            
            state = 'A'  # A for alive
                
            PredatorPopulation.append(Predator(x, y, hungry, state))
        return PredatorPopulation

    def update(self):
        """
        Perform one timestep:
        1.  Update Predator population. Move the Predators. If a Predator is
            hungry it can bite a Prey with a probability biteProb.
            Update the hungry state of the Predators.
        2.  Update the Prey population. If a Prey dies remove it from the
            population, and add a replacement Prey.
        """
        ## In here we let a predator bite a prey when they are in the same grid, the predator is faster and moves first!
        for i, predator in enumerate(self.PredatorPopulation):
            predator.move(self.height, self.width)
            for prey in self.PreyPopulation:
                if predator.position == prey.position and predator.hungry\
                   and np.random.uniform() <= self.biteProb:
                     predator.bite(prey)
                    
        """
        Set the hungry state from false to true after a
                     number of time steps has passed.
        """
        
        for i, predator in enumerate(self.PredatorPopulation):
            
            # We implement that after a certain time steps a predator gets hungry again, by checking the time they have been not hungry yet.
            predator.time_not_hungry += 1
            if predator.hungry == True:
                predator.count_hungry += 1
            if predator.time_not_hungry == self.time_before_hungry:
                predator.hungry = True
                predator.time_not_hungry = 0
        
        for j, prey in enumerate(self.PreyPopulation):
            """
            Update the Prey population.
            """      
            # If the prey is bitten, they should be removed from the model, since they are dead (now for ease we just add a new one instead of generating birth):
            if prey.state == 'D':
                self.PreyPopulation.remove(prey)
                self.list_indexes_not_had.append(prey.position)
                
                x_y = drawing_with_replacement(self.list_indexes_not_had,1)
                x = x_y[0][0]
                y = x_y[0][1]
                
                self.list_indexes_not_had.remove(x_y[0])   
                state = 'A'  # A for alive
                     
                # We add the Predator we 'created' to our population
                self.PreyPopulation.append(Prey(x, y, state))
                
            # We consider the alive preys
            if prey.state == 'A':
                
                # Our time that prey has been alive gets updated. Per time step.
                self.time_alive[j] += 1
                
            # A prey always has a random chance of dying 
                # We check wether the prey dies or not
                if np.random.uniform() <= self.mortality_rate/timeSteps:
                    
                    # If they die, we delete the prey, regenerate one and update everything else
                    prey.state = 'D'
                    self.deathPreyCount += 1
                    self.PreyPopulation.remove(prey)
                    self.list_indexes_not_had.append(prey.position)
                    
                    x_y = drawing_with_replacement(self.list_indexes_not_had,1)
                    x = x_y[0][0]
                    y = x_y[0][1]
                    
                    self.list_indexes_not_had.remove(x_y[0])   
                    state = 'A'  # A for alive
                         
                    # We add the Predator we 'created' to our population
                    self.PreyPopulation.append(Prey(x, y, state))
            
        """
        Update how there are new predators and preys born (delete whats up here than)
        """
            # Now check how they repopulate (dependant on what Miji told us, just forget for now)
                    
        """
        How the predators die (we assume they die if not eaten in time or just mortality rate)
        """
        # First we will look wether the predator has eaten in time
        for k, predator in enumerate(self.PredatorPopulation):
            
            if predator.state == 'A' and predator.count_hungry > 100: ## Determine self how many steps they need to be hungry to die
                predator.state = 'D'
                self.deathPredatorCount +=1
                
                # Again we remove it from the list and for ease immediately add a new one (again dependent on mijis method of reproducibility)
                self.PredatorPopulation.remove(predator)
                self.list_indexes_not_had.append(predator.position)
                
                x_y = drawing_with_replacement(self.list_indexes_not_had,1)
                x = x_y[0][0]
                y = x_y[0][1]
                
                if (i / self.nPredator) <= self.initPredatorHungry: # See wether the Predator is hungry or not 
                    hungry = True
                else:
                    hungry = False
                
                self.list_indexes_not_had.remove(x_y[0])   
                state = 'A'  # A for alive
                     
                # We add the Predator we 'created' to our population
                self.PredatorPopulation.append(Predator(x, y, hungry, state))
                
        # Now we will assume that they also have a mortality rate 
            # We check wether the predator dies or not
            if predator.state == 'A' and np.random.uniform() <= self.mortality_rate/timeSteps:
                
                # If they die, we delete the predator, regenerate one and update everything else
                predator.state = 'D'
                self.deathPredatorCount += 1
                self.PredatorPopulation.remove(prey)
                self.list_indexes_not_had.append(predator.position)
                
                x_y = drawing_with_replacement(self.list_indexes_not_had,1)
                x = x_y[0][0]
                y = x_y[0][1]
                
                if (i / self.nPredator) <= self.initPredatorHungry: # See wether the Predator is hungry or not 
                    hungry = True
                else:
                    hungry = False
                
                self.list_indexes_not_had.remove(x_y[0])   
                state = 'A'  # A for alive
                     
                # We add the Predator we 'created' to our population
                self.PredatorPopulation.append(Predator(x, y, hungry, state))

        """
        Update the data/statistics e.g. infectedCount,
                      deathCount, etc.
        """
        
        return self.deathPreyCount, self.deathPredatorCount, self.bornPreyCount, self.bornPredatorCount
    


class Predator:
    def __init__(self, x, y, hungry, state):
        """
        Class to model the Predators. Each Predator is initialized with a random
        position on the grid. Predators can start out hungry or not hungry.
        """
        self.position = [x, y]
        self.hungry = hungry
        self.time_not_hungry = 0 ## After a certain while the predators become hungry
        self.state = state
        self.count_hungry = 0 ## Counts for how long they have been hungry

    def bite(self, prey):
        """
        Function that handles the biting. 
        After a Predator bites it is no longer hungry.
        """
        if prey.state == 'A':
            prey.state = 'D'
            self.deathPreyCount +=1
        self.hungry = False
        self.count_hungry = 0

    def move(self, height, width): ## Still need to adjust to hunt towards prey 
        """
        Moves the Predator one step in a random direction.
        """
        deltaX = np.random.randint(-1, 2)
        deltaY = np.random.randint(-1, 2)
        """
        The Predators may not leave the grid. There are two options:
                      - fixed boundaries: if the Predator wants to move off the
                        grid choose a new valid move.
                      - periodic boundaries: implement a wrap around i.e. if
                        y+deltaY > ymax -> y = 0. This is the option currently implemented.
        """
        self.position[0] = (self.position[0] + deltaX) % width
        self.position[1] = (self.position[1] + deltaY) % height


class Prey: ## Also add movement that it moves away from predator
    def __init__(self, x, y, state):
        """
        Class to model the Preys. Each Prey is initialized with a random
        position on the grid. 
        """
        self.position = [x, y]
        self.state = state



if __name__ == '__main__':
    import time
    start_time = time.time()
    """
    Simulation parameters
    """
    fileName = 'simulation'
    
    # We had a loop for the parameter selection, but for visualization we just take in account one plot.
    n = 1
    infections = []
    for _ in range(n): 
        timeSteps = 250
        t = 0
        plotData = True
        
        last_infected = []
        """
        Run a simulation for an indicated number of timesteps.
        """
        file = open(fileName + '.csv', 'w')
        
        # We get the simullation model with the right parameters
        sim = Model(width=50, height=50, nHuman=1000, nMosquito=500,
                     initMosquitoHungry=0.6, initHumanInfected=0.02,
                     humanInfectionProb=0.6, mosquitoInfectionProb=0.2,
                     biteProb=1.0, case_fatality=0.05, prob_mosquito_starts_infected=0.1, 
                     mosquito_net_bite=0.46, mosquito_net_amount = 1000, vaccin_amount = 1, 
                     vaccin_rate = 0.66)
        
        #vis = malaria_visualize.Visualization(sim.height, sim.width)
        print('Starting simulation')
        while t < timeSteps:
            [d1, d2] = sim.update()  # Catch the data
            line = str(t) + ',' + str(d1) + ',' + str(d2) + '\n'  # Separate the data with commas
            file.write(line)  # Write the data to a .csv file
            #vis.update(t, sim.mosquitoPopulation, sim.humanPopulation)
            sim.update()
    
            t += 1

                
        file.close()
    #vis.persist()
    
        data = np.loadtxt(fileName+'.csv', delimiter=',')
        
        # We get the mean amount of the last 50 values for infected count
        infectedCount = data[:, 1]    
        infections.append(np.mean(infectedCount[-50:]))

        if plotData:
            """
            Make a plot by from the stored simulation data.
            """
            data = np.loadtxt(fileName+'.csv', delimiter=',')
            time = data[:, 0]
            infectedCount = data[:, 1]
            deathCount = data[:, 2]
            
            rounded_mean_infected = np.mean(infections)
            print(f"The mean is : {rounded_mean_infected}")
            
            # We plot everything we want, infectedcount, deathcount and the mean value line.
            plt.figure()
            plt.plot(time, infectedCount, label='infected')
            plt.plot(time, deathCount, label='deaths')

            plt.axhline(y=round(np.mean(infectedCount[-50:]),1), color='r', linestyle='--', label='mean # infected over the last 50 timesteps')
            plt.xlabel('timesteps')
            plt.ylabel('amount')
            
            plt.text(x=30, y=rounded_mean_infected + 1, s=f'y = {rounded_mean_infected}', va='bottom', ha='right', color='r')
           
            plt.grid(True, linestyle=':')
            
            plt.legend()
            plt.show()

    print(f"Mean infections: {np.mean(infections)}")
import time
end_time = time.time()
print(f"Time to run: {end_time - start_time}")
