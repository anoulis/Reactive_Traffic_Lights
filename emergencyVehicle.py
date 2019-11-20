import network

class EmergencyVehicle():
    def __init__(self, id):
        self.id = id

    def printID(self):
        print("The ID is " + self.id)
    
    def getID(self):
        return self.id

    def getPosition(self,state):
        return network.traci.vehicle.getLanePosition(self.id) 

    def getLane(self):
        return network.traci.vehicle.getLaneID(self.id) 