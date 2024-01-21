# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:18:46 2024

@author: luukv
"""

import matplotlib.pyplot as plt
import numpy as np
import vis_code_luuk

class Model: 
    def __init__(self, width=100, height=100, nHares=700, nLynx=4, huntDistance=5, killProb=0.5, breedDistLynx = 3, breedDistHares = 0, breedProbHares = 0.01, breedProbLynx = 0.1):
        """
        Model parameters
        Initialize the model with the width and height parameters.
        """
        self.height = height
        self.width = width
        self.nHares = nHares
        self.nLynx = nLynx
        self.killProb = killProb
        self.breedDistLynx = breedDistLynx
        self.breedDistHares = breedDistHares
        self.breedProbHares = breedProbHares
        self.breedProbLynx = breedProbLynx
        self.huntDistance = huntDistance
        # etc. 

        """
        Data parameters
        To record the evolution of the model
        """
        self.LynxDeathCount = 0
        self.HaresDeathCount = 0
        # etc.

        """
        Population setters
        Make a data structure in this case a list with the hares and lynx.
        """
        self.HaresPopulation = self.set_hare_population()
        self.LynxPopulation = self.set_lynx_population()

    def set_hare_population(self):
        """
        This function makes the initial Hare population, by iteratively adding
        an object of the Hare class to the harePopulation list.
        The position of each Hare object is randomized.
        """
        harePopulation = []
        for i in range(self.nHares):
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            """
            Hares may have overlapping positions.
            """
            if np.random.uniform() < 0.5:
                state = 'M'  # M for male
            else:
                state = 'F' # F for female
            time_born = 0
                
            harePopulation.append(Hare(x, y, state, self, time_born))
        return harePopulation

    def set_lynx_population(self):
        """
        This function makes the initial lynx population, by iteratively
        adding an object of the Lynx class to the lynxPopulation list.
        The position of each Mosquito object is randomized.
        """
        lynxPopulation = []
        for i in range(self.nLynx):
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            if np.random.uniform() < 0.5:
                state = 'M'  # M for male
            else:
                state = 'F' # F for female
            
            time_born = 0
            hungry = 0
            time_hungry = 0

            lynxPopulation.append(Lynx(x, y, state, self, time_born, hungry, time_hungry))
        return lynxPopulation

    def update(self):
        """
        Perform one timestep:
        1.  Update hares population. Move the hares. If a lynx is
            hungry it can bite a hares with a probability biteProb.
            Update the hungry state of the hares.
        2.  Update the lynx population. If a lynx dies remove it from the
            population, and add a replacement lynx.
        """
        
        for i, l in enumerate(self.LynxPopulation):
            l.move(self.height, self.width)
            l.time_born += 1
            
            if l.time_born == 60: ## After a year
                if np.random.uniform() < 0.5:
                    l.state = 'M' 
                else:
                    l.state = 'F'
        
            for h in self.HaresPopulation:
                if abs(l.position[0] - h.position[0]) <= self.huntDistance and abs(l.position[1] - h.position[1] <= self.huntDistance): # adjust to closeby 
                    if l.state == 'M' or l.state == 'F' or l.state == 'B':
                        l.hunt(h, self.killProb)

        for j, h in enumerate(self.HaresPopulation):
            """
            Update the hares population. Let them all move around. Also add when a hare
            is old enough and becomes an adult (either female or male).
            """
            h.move(self.height,self.width)
            if h.state == 'B':
                h.time_born += 1
            if h.time_born == 30: ## After a month
                if np.random.uniform() < 0.5:
                    h.state = 'M' 
                else:
                    h.state = 'F'
                               
        for j, h1 in enumerate(self.HaresPopulation):
            """
            Update the population of hares, let them reproduce if possible.
            """
            for k, h2 in enumerate(self.HaresPopulation): 
                if h1.position == h2.position and h1.state == "M" and h2.state == "F" \
                    and (t - h1.lastbreed and t - h2.lastbreed) > 30:
                        h1.breed(h2, self.breedProbHares)

        
        for m, l1 in enumerate(self.LynxPopulation):
            """
            Update the population of lynx, let them reproduce if possible.
            """
            for n, l2 in enumerate(self.LynxPopulation):
                if abs(l1.position[0] - l1.position[0]) <= self.breedDistLynx \
                    and abs(l1.position[1] - l2.position[1] <= self.breedDistLynx) \
                        and l1.state == 'M' and l2.state == 'F' \
                            and ((t - l1.lastbreed and t - l2.lastbreed) > 90 or l1.lastbreed==l2.lastbreed==0):
                    l1.breed(l2, self.breedProbLynx)
                
                            
        """
        Update the data/statistics e.g. infectedCount,
                      deathCount, etc.
        Reset the Lynx to be hungry again
        Lynx die of starvation if not eaten enough
        """
        eaten_list = []
        saturation_list = []
        for o, l in enumerate (self.LynxPopulation):
            l.eathistory.append(l.hungry)
            eaten_list.append(l.eathistory[-1:])
            
            saturation_list.append(sum(l.eathistory[-30:]))
            
            if sum(l.eathistory[-30:]) < 7 and l.time_born > 30:
                self.LynxDeathCount += 1
                self.LynxPopulation.remove(l)
                    
            l.hungry = 0
          
        PreyAvailability = np.mean(eaten_list)
        SaturationLynx = np.mean(saturation_list)
        return len(self.LynxPopulation), len(self.HaresPopulation), PreyAvailability, SaturationLynx


class Lynx:
    def __init__(self, x, y, state, model, time_born, hungry, time_hungry):
        """
        Class to model the lynx. Each lynx is initialized with a random
        position on the grid.
        """
        self.position = [x, y]
        self.model = model
        self.state = state
        self.time_born = time_born
        self.hungry = hungry
        self.time_hungry = time_hungry
        self.eathistory = []
        self.lastbreed = 0

    def hunt(self, hare, killProb):
        """
        Function that handles the biting. If the hares is infected and the
        target hares is susceptible, the hares can be infected.
        If the lynx is not infected and the target hares is infected, the
        lynx can be infected.
        After a hares hunts and kills, it will add its hares to its eaten tally. If it has
        eaten 3 hares, it wont kill any other hares nearby.
        """
        if np.random.uniform() <= killProb and self.hungry < 1:
            self.model.HaresDeathCount += 1
            self.model.HaresPopulation.remove(hare)
            self.hungry +=1
            self.time_hungry = 0


    def move(self, height, width):
        """
        Moves the lynx one step in a random direction.
        """
        speed_increase=1
        self.huntDistance = 4
        
        deltaX = np.random.randint(-3, 4)
        deltaY = np.random.randint(-3, 4)
        
        if np.sum(self.eathistory[-10:]) < 3 and self.time_born > 10:
            self.huntDistance = 6
            
        if np.sum(self.eathistory[-20:]) < 7 and self.time_born > 20:
            if np.random.uniform() < 0.2:
                speed_increase = 2
            self.huntDistance= 8
        """
        The hares may not leave the grid. There are two options:
                      - fixed boundaries: if the lynx wants to move off the
                        grid choose a new valid move.
                      - periodic boundaries: implement a wrap around i.e. if
                        y+deltaY > ymax -> y = 0. This is the option currently implemented.
        """
        if self.time_born % 7 == 0:
            self.xdirection = deltaX
            self.ydirection = deltaY
        
        self.position[0] = (self.position[0] + self.xdirection*speed_increase) % width
        self.position[1] = (self.position[1] + self.ydirection*speed_increase) % height
    
    def breed(self, lynx2, breedProbLynx):
        """
        Determines whether two nearby female and male lynx actually reproduce or not.
        """
        if np.random.uniform() <= breedProbLynx:
            x = self.position[0]
            y = self.position[1]
            """
            Lynx may have overlapping positions.
            """
            
            self.lastbreed = 1 if t==0 else t
            lynx2.lastbreed = 1 if t==0 else t
            
            state = 'B'  # B for baby
            time_born = 0
            hungry = 0
            time_hungry = 0
            self.model.LynxPopulation.append(Lynx(x, y, state, self.model, time_born, hungry, time_hungry))


class Hare:
    def __init__(self, x, y, state, model, time_born):
        """
        Class to model the hares. Each hare is initialized with a random
        position on the grid. Hares start out neutral for now.
        """
        self.position = [x, y]
        self.state = state
        self.model = model
        self.time_born = 0
        self.lastbreed = 0
     
    def move(self, height, width):
        """
        Moves the hares one step in a random direction.
        """
        deltaX = np.random.randint(-1, 2)
        deltaY = np.random.randint(-1, 2)
        """
        The hares may not leave the grid. There are two options:
                      - fixed boundaries: if the hares wants to move off the
                        grid choose a new valid move.
                      - periodic boundaries: implement a wrap around i.e. if
                        y+deltaY > ymax -> y = 0. This is the option currently implemented.
        """
        self.position[0] = (self.position[0] + deltaX) % width
        self.position[1] = (self.position[1] + deltaY) % height
    
    def breed(self, hare2, breedProbHares):
        """
        Determines whether two nearby female and male hares actually reproduce or not.
        """
        if np.random.uniform() <= breedProbHares:
            x = self.position[0]
            y = self.position[1]
            """
            Hares may have overlapping positions.
            """
            self.lastbreed = t
            hare2.lastbreed = t
            
            state = 'B'  # B for baby
            time_born = 0
            self.model.HaresPopulation.append(Hare(x, y, state, self.model, time_born))
            

if __name__ == '__main__':
    """
    Simulation parameters
    """
    fileName = 'simulation'
    timeSteps = 400
    t = 0
    plotData = True
    """
    Run a simulation for an indicated number of timesteps.
    """
    file = open(fileName + '.csv', 'w')
    sim = Model(breedProbHares=0.9, breedProbLynx=0.7, nHares=1500, nLynx = 6, killProb=1, \
                huntDistance=5, breedDistLynx=20, breedDistHares=1)
    vis = vis_code_luuk.Visualization(sim.height, sim.width)
    print('Starting simulation')
    while t < timeSteps:
        [d1, d2, d3, d4] = sim.update()  # Catch the data
        sim.update()  # Catch the data
        line = str(t) + ',' + str(d1) + ',' + str(d2) + ',' + str(d3) + ',' + str(d4) +  '\n'  # Separate the data with commas
        file.write(line)  # Write the data to a .csv file
        vis.update(t, sim.LynxPopulation, sim.HaresPopulation)
        t += 1
    file.close()
    vis.persist()

    if plotData:
        """
        Make a plot by from the stored simulation data.
        """
        data = np.loadtxt(fileName+'.csv', delimiter=',')
        time = data[:, 0]
        LynxAmount = data[:, 1]
        HaresAmount = data[:, 2]
        PreyAvailability = data[:, 3]
        LynxSaturation = data[:, 4]
        
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(10, 6))

        ax1.plot(time, LynxAmount, label='Lynx Population')
        ax1.legend()

        ax2.plot(time, HaresAmount, label='Hazes Population')
        ax2.legend()
        
        ax3.plot(time, PreyAvailability, label='Prey Availability')
        ax3.legend()
        
        ax4.plot(time, LynxSaturation, label='Lynx Saturation')
        ax4.legend()
        
        plt.tight_layout()
        plt.show()