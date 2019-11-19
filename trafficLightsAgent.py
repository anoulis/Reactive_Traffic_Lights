import network

class TrafficLightAgent():
    def __init__(self, id):
        self.id = id

    def printID(self):
        print("The ID is " + self.id)
    
    def getID(self):
        return self.id
    '''

    def setCustomLights(self,state):
        network.traci.trafficlight.setRedYellowGreenState(self.id,state)

    def setPhase(self,phase):
        network.traci.trafficlight.setPhase(self.id,phase)


    def getPhase():

    
    def setLastPhase():

    
    def getLastPhase():


    def getControlledLanes(self):
        return network.traci.trafficlight.getControlledLanes(self.id)
    
    def getControlledLinks(self):
        return network.traci.trafficlight.getControlledLinks(self.id)
    
    def getCompleteRedYellowGreenDefinition():

    def getNextSwitch():

    def setCompleteRedYellowGreenDefinition():

            
    tl_list = []
    for i in getAllLightIds():
        tl_list.append(trafficLightsAgent.TrafficLightAgent(str(i)))
    
    for tl in tl_list:
        tl.printID()

    '''

    

    