import network

class TrafficLightAgent():

    def __init__(self, id):
        self.id = id
        self.behaviour = "normal"


    def printID(self):
        print("The ID is " + self.id)
    
    def getID(self):
        return self.id

    
    def setCustomLights(self,state):
        network.traci.trafficlight.setRedYellowGreenState(self.id,state)

    def setPhase(self,phase):
        network.traci.trafficlight.setPhase(self.id,phase)

    def getControlledLanes(self):
        return network.traci.trafficlight.getControlledLanes(self.id)
    
    def getControlledLinks(self):
        return network.traci.trafficlight.getControlledLinks(self.id)

    

    

    