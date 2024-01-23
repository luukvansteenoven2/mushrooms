# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:58:08 2024

@author: trist
"""

import matplotlib.pyplot as plt
import numpy as np
import vis_code_luuk

class Model: 
    def __init__(self, width=100, height=100, nHares=500, nLynx=6, killProb=0.8, breedDistLynx = 20, breedDistHares = 1, breedProbHares = 0.1, breedProbLynx = 0.00001, maximumHares = 2500, maximumLynx = 20):
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
        self.maxLynx = maximumLynx
        self.maxHares = maximumHares

        """
        Data parameters
        To record the evolution of the model
        """
        self.LynxDeathCount = 0
        self.HaresDeathCount = 0

        """
        Population setters
        Make a data structure in this case a list with the hares and lynx.
        """
        self.HaresPopulation = self.set_hare_population()
        self.LynxPopulation = self.set_lynx_population()
        self.environment = self.initialize_environment()

    def initialize_environment(self):
        # Initialize your environment grid
        # For simplicity, 0 could represent plain land, and 1 could represent mountains
        env = np.zeros((self.height, self.width))
        # Set up mountains in the environment
        # This could be random or based on some pattern
        env[10:40, 30:50] = 1  # creates a 10x10 mountain block
        return env

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
                
            harePopulation.append(Hare(x, y, state, self))
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

            lynxPopulation.append(Lynx(x, y, state, self))
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
        
        """
        Neither populations will die out, also there will be a maximum capacity,
        due to food limitations in reality
        """
        if len(self.LynxPopulation) <= 2:
            for p, l in enumerate(self.LynxPopulation):
                l.eathistory.append(1)
        if len(self.HaresPopulation) <= 20:
            killProbHares = 0
       # else:
        killProbHares = self.killProb
        
        for i, l in enumerate(self.LynxPopulation):
            l.move(self.height, self.width)
            l.time_born += 1
            
            if l.time_born == 150: ## After a year
                if np.random.uniform() < 0.5:
                    l.state = 'M' 
                else:
                    l.state = 'F'
        
            for h in self.HaresPopulation:
                if abs(l.position[0] - h.position[0]) <= l.huntDistance and abs(l.position[1] - h.position[1] <= l.huntDistance): # adjust to closeby 
                    if l.state == 'M' or l.state == 'F' or l.state == 'B':
                        l.hunt(h, killProbHares)

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
        
        if len(self.HaresPopulation) >= self.maxHares:
            probbreedHares = self.breedProbHares/(len(self.LynxPopulation)*0.5) * 0.1
        else:
            probbreedHares = self.breedProbHares/(len(self.LynxPopulation))
        
       # if len(self.LynxPopulation) >= self.maxLynx:
        #    probbreedLynx = 0
       # else:
        probbreedLynx = self.breedProbLynx * (len(self.HaresPopulation)*2)
        
                               
       # for j, h1 in enumerate(self.HaresPopulation):
       #     """
       #     Update the population of hares, let them reproduce if possible.
       #     Let there be a maximum capacity of hares, than the breed probability will be 0
        #    """
        #    for k, h2 in enumerate(self.HaresPopulation): 
       #         if h1.position == h2.position and h1.state == "M" and h2.state == "F" \
        #            and (t - h1.lastbreed and t - h2.lastbreed) > 30:
        #                h1.breed(h2, probbreedHares)
    
        for m, h in enumerate(self.HaresPopulation):
            """
            Let the Hares reproduce by themselves.
            """
            if h.state == 'F' or h.state == 'M':
                h.breed(probbreedHares)
                               
     #   for m, l1 in enumerate(self.LynxPopulation):
     #       """
     #       Update the population of lynx, let them reproduce if possible.
     #       """
     #       for n, l2 in enumerate(self.LynxPopulation):
     #           if abs(l1.position[0] - l1.position[0]) <= self.breedDistLynx \
     #               and abs(l1.position[1] - l2.position[1] <= self.breedDistLynx) \
     #                   and l1.state == 'M' and l2.state == 'F' \
      #                      and ((t - l1.lastbreed and t - l2.lastbreed) > 90 or l1.lastbreed==l2.lastbreed==0):
      #              l1.breed(l2, self.breedProbLynx)
        
        for m, l in enumerate(self.LynxPopulation):
            """
            Let the lynx reproduce by themselves.
            """
            if l.state == 'M' or l.state == 'F':
                l.breed(probbreedLynx)
                
        """
        Update the data/statistics e.g. infectedCount,
                      deathCount, etc.
        Reset the Lynx to be hungry again
        Lynx die of starvation if not eaten enough, they need to atleast eat 3 hares in the last
        14 timesteps to survive.
        """
        eaten_list = []
        saturation_list = []
        for o, l in enumerate(self.LynxPopulation):
            l.eathistory.append(l.hungry)
            eaten_list.append(l.eathistory[-1:])
            
            saturation_list.append(sum(l.eathistory[-14:]))
            
            if sum(l.eathistory[-14:]) < 3 and l.time_born > 30:
                self.LynxDeathCount += 1
                self.LynxPopulation.remove(l)
                    
            l.hungry = 0
           
        PreyAvailability = np.mean(eaten_list)
        SaturationLynx = np.mean(saturation_list)
        
        return len(self.LynxPopulation), len(self.HaresPopulation), PreyAvailability, SaturationLynx


class Lynx:
    def __init__(self, x, y, state, model):
        """
        Class to model the lynx. Each lynx is initialized with a random
        position on the grid.
        """
        self.position = [x, y]
        self.model = model
        self.state = state
        self.time_born = 0
        self.hungry = 0
        self.time_hungry = 0
        self.eathistory = []
        self.lastbreed = 0
        self.huntDistance = 3
        self.speed = 1

    def hunt(self, hare, killProb):
        """
        Function that handles the biting. If the hares is infected and the
        target hares is susceptible, the hares can be infected.
        If the lynx is not infected and the target hares is infected, the
        lynx can be infected.
        After a hares hunts and kills, it will add its hares to its eaten tally. If it has
        eaten 3 hares, it wont kill any other hares nearby.
        """
        if np.random.uniform() <= killProb and self.hungry < 3:
            self.model.HaresDeathCount += 1
            self.model.HaresPopulation.remove(hare)
            self.hungry +=1
            self.time_hungry = 0


    def move(self, height, width):
        """
        Moves the lynx one step in a random direction. The more hungry the lynxes are, the 'intenser'
        they will hunt.
        """      
        deltaX = np.random.randint(-2, 3)
        deltaY = np.random.randint(-2, 3)
        
        if np.sum(self.eathistory[-3:]) < 3 and self.time_born > 10:
            self.huntDistance = 6
            
        if np.sum(self.eathistory[-7:]) < 3 and self.time_born > 20:
            #if np.random.uniform() < 0.2:
            self.speed = 2
            self.huntDistance = 8
        
        else:
            self.speed = 1
            self.huntDistance = 3
            
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
        
        self.position[0] = (self.position[0] + self.xdirection*self.speed) % width
        self.position[1] = (self.position[1] + self.ydirection*self.speed) % height
    
    def breed(self, breedProbLynx):
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
            #lynx2.lastbreed = 1 if t==0 else t
            
            state = 'B'  # B for baby
            self.model.LynxPopulation.append(Lynx(x, y, state, self.model))


class Hare:
    def __init__(self, x, y, state, model):
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
        deltaX = np.random.randint(-2, 3)
        deltaY = np.random.randint(-2, 3)
        """
        The hares may not leave the grid. There are two options:
                      - fixed boundaries: if the hares wants to move off the
                        grid choose a new valid move.
                      - periodic boundaries: implement a wrap around i.e. if
                        y+deltaY > ymax -> y = 0. This is the option currently implemented.
        """
        self.position[0] = (self.position[0] + deltaX) % width
        self.position[1] = (self.position[1] + deltaY) % height
    
    def breed(self, breedProbHares):
        """
        Determines whether two nearby female and male hares actually reproduce or not. We include
        the fact that hares reproduce worse when lynx population amount increases
        """
        if np.random.uniform() <= breedProbHares:
            x = self.position[0]
            y = self.position[1]
            """
            Hares may have overlapping positions.
            """
            self.lastbreed = t
           # hare2.lastbreed = t
            
            state = 'B'  # B for baby
            self.model.HaresPopulation.append(Hare(x, y, state, self.model))
            
state=0
if __name__ == '__main__':
    """
    Simulation parameters
    """
    np.random.seed(state)
    fileName = 'simulation'
    timeSteps = 200
    t = 0
    plotData = True
    """
    Run a simulation for an indicated number of timesteps.
    """
    file = open(fileName + '.csv', 'w')
    sim = Model(nHares=500)
    vis = vis_code_luuk.Visualization(sim.height, sim.width)
    print('Starting simulation')
    while t < timeSteps:
        [d1, d2, d3, d4] = sim.update()  # Catch the data
        sim.update()  # Catch the data
        line = str(t) + ',' + str(d1) + ',' + str(d2) + ',' + str(d3) + ',' + str(d4) +  '\n'  # Separate the data with commas
        file.write(line)  # Write the data to a .csv file
        vis.update(t, sim.LynxPopulation, sim.HaresPopulation, sim.environment)
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