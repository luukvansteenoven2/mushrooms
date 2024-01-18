# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:18:46 2024

@author: luukv
"""

import matplotlib.pyplot as plt
import numpy as np
import vis_code_luuk


class Model:
    def __init__(self, width=50, height=50, nHares=1, nLynx=10, killProb=1.0):
        """
        Model parameters
        Initialize the model with the width and height parameters.
        """
        self.height = height
        self.width = width
        self.nHares = nHares
        self.nLynx = nLynx
        self.killProb = killProb
        # etc.

        """
        Data parameters
        To record the evolution of the model
        """
        self.deathCount = 0
        self.HaresDeathCount = 0
        # etc.

        """
        Population setters
        Make a data structure in this case a list with the humans and mosquitos.
        """
        self.HaresPopulation = self.set_hare_population()
        self.LynxPopulation = self.set_lynx_population()

    def set_hare_population(self):
        """
        This function makes the initial human population, by iteratively adding
        an object of the Human class to the humanPopulation list.
        The position of each Human object is randomized. A number of Human
        objects is initialized with the "infected" state.
        """
        harePopulation = []
        for i in range(self.nHares):
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            """
            To implement: Humans may not have overlapping positions.
            """
            state = 'N'  # N for neutral
            harePopulation.append(Hare(x, y, state))
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

            lynxPopulation.append(Lynx(x, y, self))
        return lynxPopulation

    def update(self):
        """
        Perform one timestep:
        1.  Update mosquito population. Move the mosquitos. If a mosquito is
            hungry it can bite a human with a probability biteProb.
            Update the hungry state of the mosquitos.
        2.  Update the human population. If a human dies remove it from the
            population, and add a replacement human.
        """
        for i, l in enumerate(self.LynxPopulation):
            l.move(self.height, self.width)
            for h in self.HaresPopulation:
                if abs(l.position[0] - h.position[0]) < 5 and abs(l.position[1] - h.position[1]) < 5:
                    l.hunt(h, self.killProb)
        """
        To implement: set the hungry state from false to true after a
                     number of time steps has passed.
        """

        for j, h in enumerate(self.HaresPopulation):
            h.move(self.height, self.width)
            """
            To implement: update the human population.
            """

        """
        To implement: update the data/statistics e.g. infectedCount,
                      HaresDeathCount, etc.
        """
        
        
        return self.HaresDeathCount


class Lynx:
    def __init__(self, x, y, model):
        """
        Class to model the lynx. Each lynx is initialized with a random
        position on the grid.
        """
        self.position = [x, y]
        self.model = model
        #self.hungry = 

    def hunt(self, hare, killProb):
        """
        Function that handles the biting. If the mosquito is infected and the
        target human is susceptible, the human can be infected.
        If the mosquito is not infected and the target human is infected, the
        mosquito can be infected.
        After a mosquito bites it is no longer hungry.
        """
        if np.random.uniform() <= killProb:
            self.model.HaresDeathCount += 1 
            self.model.HaresPopulation.remove(hare)
        
        return

    def move(self, height, width):
        """
        Moves the mosquito one step in a random direction.
        """
        deltaX = np.random.randint(-1, 2)
        deltaY = np.random.randint(-1, 2)
        """
        The mosquitos may not leave the grid. There are two options:
                      - fixed boundaries: if the mosquito wants to move off the
                        grid choose a new valid move.
                      - periodic boundaries: implement a wrap around i.e. if
                        y+deltaY > ymax -> y = 0. This is the option currently implemented.
        """
        self.position[0] = (self.position[0] + deltaX) % width
        self.position[1] = (self.position[1] + deltaY) % height


class Hare:
    def __init__(self, x, y, state):
        """
        Class to model the hares. Each hare is initialized with a random
        position on the grid. Hares start out neutral for now.
        """
        self.position = [x, y]
        self.state = state

    def move(self, height, width):
        """
        Moves the mosquito one step in a random direction.
        """
        deltaX = np.random.randint(-1, 2)
        deltaY = np.random.randint(-1, 2)
        """
        The mosquitos may not leave the grid. There are two options:
                      - fixed boundaries: if the mosquito wants to move off the
                        grid choose a new valid move.
                      - periodic boundaries: implement a wrap around i.e. if
                        y+deltaY > ymax -> y = 0. This is the option currently implemented.
        """
        self.position[0] = (self.position[0] + deltaX) % width
        self.position[1] = (self.position[1] + deltaY) % height





if __name__ == '__main__':
    """
    Simulation parameters
    """
    fileName = 'simulation'
    timeSteps = 50
    t = 0
    plotData = False
    """
    Run a simulation for an indicated number of timesteps.
    """
    file = open(fileName + '.csv', 'w')
    sim = Model()
    vis = vis_code_luuk.Visualization(sim.height, sim.width)
    print('Starting simulation')
    while t < timeSteps:
        #[d1] = sim.update()  # Catch the data
        #line = str(t) + ',' + str(d1) + ',' + '\n'  # Separate the data with commas
        #file.write(line)  # Write the data to a .csv file
        sim.update()
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
        infectedCount = data[:, 1]
        deathCount = data[:, 2]
        plt.figure()
        plt.plot(time, infectedCount, label='infected')
        plt.plot(time, deathCount, label='deaths')
        plt.legend()
        plt.show()