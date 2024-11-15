#By: Jack Aldworth
#Made: 9/27/2024
#An edited version of the Genetic Evolutionary Algorithem made by Eduardo Izquierdo
import numpy as np
import matplotlib.pyplot as plt

class MGA():

    def __init__(self, ff, gs, ps, rcp, mp, t):
        #given variables
        self.genesize = gs
        self.popsize = ps
        self.recomprob = rcp
        self.mutationprob = mp
        self.tournaments = t
        self.fitnessfunction = ff
        self.pop = np.random.random((ps,gs))*2 - 1
        #variables to store fitness
        self.fitness = np.zeros(ps)
        self.fValid = np.zeros(ps)
        # stats variables
        gens = t//ps      
        self.bestfit = np.zeros(gens)
        self.avgfit = np.zeros(gens)
        self.bestind = np.zeros(gens)

    def getFitness(self,index):
        if(self.fValid[index] == 1):
            return self.fitness[index]
        self.fitness[index] = self.fitnessfunction(self.pop[index])
        self.fValid[index] = 1
        return self.fitness[index]

    def run(self):
        # begin tournament Loop
        gen = 0
        for t in range(self.tournaments):
            # pick two to fight
            a = 0
            b = 0
            while(a==b):
                [a,b] = np.random.choice(np.arange(self.popsize),2,replace=False)
            # determine winner
            if self.getFitness(a) > self.getFitness(b):
                winner = a
                loser = b
            else:
                winner = b
                loser = a
            # infect loser with winners genes
            for g in range(self.genesize):
                if np.random.random() < self.recomprob: 
                    self.pop[loser][g] = self.pop[winner][g] 
            # mutate loser
            self.pop[loser] += np.random.normal(0,self.mutationprob,self.genesize)
            self.pop[loser] = np.clip(self.pop[loser],-1,1)
            #flag as changed
            self.fValid[loser] = 0
            # 6 Stats 
            if t % self.popsize == 0:
                for i in range(self.popsize):
                    self.getFitness(i)
                self.bestfit[gen] = np.max(self.fitness)
                self.avgfit[gen] = np.mean(self.fitness)
                self.bestind[gen] = np.argmax(self.fitness)
                gen += 1

    def showFitness(self):
        plt.plot(self.bestfit,label="Best")
        plt.plot(self.avgfit,label="Avg.")
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.title("Evolution")
        plt.legend()
        plt.show()
