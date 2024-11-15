import numpy as np
import matplotlib.pyplot as plt
import fnn 
import ea
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as ps
import time

#Parameters of the NN
layers = [4,16,16,4]
duration = 2000

#Parameters of the EA
genesize = np.sum(np.multiply(layers[1:],layers[:-1])) + np.sum(layers[1:]) 
print("Number of parameters:",genesize)
popsize = 10
recombProb = 0.5
mutatProb = 0.01
tournaments = 100*popsize

def walker(genotype):
    # Create the neural network.
    a = fnn.FNN(layers)

    # Set the parameters of the neural network according to the genotype.
    a.setParams(genotype)

    #setup 3D sim
    physicsClient = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0,0,-9.8)
    planeId = p.loadURDF("plane.urdf")
    robotId = p.loadURDF("walker.urdf")

    ps.Prepare_To_Simulate(robotId)
    outputs = [0.0,0.0,0.0,0.0]
    for j in range(duration):
        ps.Set_Motor_For_Joint(bodyIndex = robotId, 
                               jointName = b'LF_Motor',
                               controlMode = p.POSITION_CONTROL,
                               targetPosition = outputs[0],
                               maxForce = 500)
        ps.Set_Motor_For_Joint(bodyIndex = robotId, 
                               jointName = b'RF_Motor',
                               controlMode = p.POSITION_CONTROL,
                               targetPosition = outputs[1],
                               maxForce = 500)
        ps.Set_Motor_For_Joint(bodyIndex = robotId, 
                               jointName = b'LB_Motor',
                               controlMode = p.POSITION_CONTROL,
                                targetPosition = outputs[2],
                               maxForce = 500)
        ps.Set_Motor_For_Joint(bodyIndex = robotId,
                               jointName = b'RB_Motor',
                               controlMode = p.POSITION_CONTROL,
                               targetPosition = outputs[3],
                               maxForce = 500)
        p.stepSimulation()
        time.sleep(1/500)

        outputs = a.think(outputs)[0]

        #calculate fitness
        if (j == duration - 1):
            pos, _ = (p.getBasePositionAndOrientation(robotId))
            score = np.sqrt(pos[0]*pos[0]+pos[1]*pos[1])
            p.disconnect()

    return score
    

# Evolve
ga = ea.MGA(walker, genesize, popsize, recombProb, mutatProb, tournaments)
ga.run()
ga.showFitness()
