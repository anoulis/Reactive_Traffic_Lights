import network

class LanesAgent():
    def __init__(self, id):
        self.id = id
        self.fixed_id = id+"_0"

    def printID(self):
        print("The ID is " + self.id)
    
    def getID(self):
        return self.id

    def getFixedID(self):
        return self.fixed_id

    def getLaneLength(self):
        return network.traci.lane.getLength(self.fixed_id)
    
    def getLaneWaitingTime(self):
        return network.traci.lane.getWaitingTime(self.fixed_id)