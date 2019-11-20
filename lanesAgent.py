import network

class LanesAgent():
    def __init__(self, id):
        self.id = id

    def printID(self):
        print("The ID is " + self.id)
    
    def getID(self):
        return self.id

    def getLaneLength(self):
        return network.traci.lane.getLength(self.id)
    
    def getLaneWaitingTime(self):
        return network.traci.lane.getWaitingTime(self.id)