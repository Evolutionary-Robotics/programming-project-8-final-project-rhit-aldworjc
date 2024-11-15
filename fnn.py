#By: Jack Aldworth
#Made: 9/27/2024
#An edited version of the neural network made by Eduardo Izquierdo
import numpy as np

class FNN:
    def __init__(self, units_per_layer):
        
        #given variables
        self.units_per_layer = units_per_layer
        self.num_layers = len(units_per_layer)

        # lambdas for supported activation functions
        self.activation = lambda x: 1 / (1 + np.exp(-x))

        self.weightrange = 5
        self.biasrange = 5

    def setRanges(self, w, b):
        self.weightrange = w
        self.biasrange = b

    def setParams(self, params):
        
        self.weights = []
        start = 0
        for l in np.arange(self.num_layers-1):
            end = start + self.units_per_layer[l]*self.units_per_layer[l+1]
            self.weights.append((params[start:end]*self.weightrange).reshape(self.units_per_layer[l],self.units_per_layer[l+1]))
            start = end
        self.biases = []
        for l in np.arange(self.num_layers-1):
            end = start + self.units_per_layer[l+1]
            self.biases.append((params[start:end]*self.biasrange).reshape(1,self.units_per_layer[l+1]))
            start = end

    def think(self, inputs):
        states = np.asarray(inputs)
        for l in np.arange(self.num_layers - 1):
            if states.ndim == 1:
                states = [states]
            states = self.activation(np.matmul(states, self.weights[l]) + self.biases[l])
        return states


