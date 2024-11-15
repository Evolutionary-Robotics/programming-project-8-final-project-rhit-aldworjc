import pybullet as p
import pybullet_data
import pyrosim.pyrosim as ps
import numpy as np
import matplotlib.pyplot as plt
import time

#parameters
numGenerations = 50
duration = 2000
mutationprob = 0.1

#setup NN
weights = np.random.random(8)*10 -5
#weights = [5,5,5,5,5,5,5,5]

bestWeights = weights
bestScore = 0
failedEvolutons = 1
#Start Evolution
x = np.linspace(0,10*np.pi, duration)
yplot = np.zeros(numGenerations)
bplot = np.zeros(numGenerations)
for i in range(numGenerations):
    print("Gen: ",i+1," of ",numGenerations)
    rf = np.sin(weights[0]*x)*np.pi/weights[1]
    lf = -np.sin(weights[0]*x+np.pi/weights[2])*np.pi/weights[3]
    rb = np.sin(weights[0]*x+np.pi/weights[4])*np.pi/weights[5]
    lb = -np.sin(weights[0]*x+np.pi/weights[6])*np.pi/weights[7]

    #setup 3D sim
    physicsClient = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0,0,-9.8)
    planeId = p.loadURDF("plane.urdf")
    robotId = p.loadURDF("walker.urdf")

    ps.Prepare_To_Simulate(robotId)

    for j in range(duration):
        ps.Set_Motor_For_Joint(bodyIndex = robotId, 
                               jointName = b'LF_Motor',
                               controlMode = p.POSITION_CONTROL,
                               targetPosition = lf[j],
                               maxForce = 500)
        ps.Set_Motor_For_Joint(bodyIndex = robotId, 
                               jointName = b'RF_Motor',
                               controlMode = p.POSITION_CONTROL,
                               targetPosition = rf[j],
                               maxForce = 500)
        ps.Set_Motor_For_Joint(bodyIndex = robotId, 
                               jointName = b'LB_Motor',
                               controlMode = p.POSITION_CONTROL,
                                targetPosition = lb[j],
                               maxForce = 500)
        ps.Set_Motor_For_Joint(bodyIndex = robotId,
                               jointName = b'RB_Motor',
                               controlMode = p.POSITION_CONTROL,
                               targetPosition = rb[j],
                               maxForce = 500)
        p.stepSimulation()
        time.sleep(1/500)

        #calculate fitness
        if (j == duration - 1):
            pos, _ = (p.getBasePositionAndOrientation(robotId))
            score = np.sqrt(pos[0]*pos[0]+pos[1]*pos[1])
            print("fitness: ",score)
            yplot[i] = score

            #check if better then previous generation
            if(score > bestScore):
                bestWeights = weights
                bestScore = score
                failedEvolutions = 1

            else:
                failedEvolutions += 1
                
            bplot[i] = bestScore
            
            weights = bestWeights
            weights += np.random.normal(0,mutationprob*failedEvolutons,8)
            weights = np.clip(weights,-10,10)
                

                
        
    #close Sim
    p.disconnect()
        
plt.plot(yplot,label='Fitness')
plt.plot(bplot,label='Parent Fitness')
plt.xlabel('generation')
plt.ylabel('fitness')
plt.legend()
plt.show()

    

