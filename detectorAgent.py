import network

class DetectorAgent():
    def __init__(self, id):
        self.id = "det_"+id

    def printID(self):
        print("The ID is " + self.id)
    
    def getID(self):
        return self.id

    def isEmergencyVehicleHere(self):
        det_vehs = network.traci.inductionloop.getLastStepVehicleIDs(self.id)
        for veh in det_vehs:
            if veh == "0ev":
                return True
            return False

