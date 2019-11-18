#!/usr/bin/env python

import os
import sys
import optparse
import subprocess
import random


# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sys.path.append('/home/jonny-smyth/Desktop/sumo/tools')

#chesare9000
#MAC -> export SUMO_HOME="/usr/local/opt/sumo/share/sumo
#UBT -> sys.path.append('/home/chesare9000/Documents/MAS/1.Traffic/sumo/tools')

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# Getters (Sensors)

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def getEmPos():
    emPos = traci.vehicle.getRoadID('0ev')
    #return the road id
    return emPos

def getLightState(lightsID):
    light = traci.trafficlight.getRedYellowGreenState(lightsID)
    #returns the lights at the intersection values
    return light

def getNumberOfVehicles(laneID):
    no_vehs = traci.lane.getLastStepVehicleNumber(laneID)
    #returns the number of vehicles in the lane ID
    return no_vehs

def getAllLightIds():
    lightList = traci.trafficlight.getIDList()
    #returns full list of lights ID in the env.
    return lightList

def getRoute(routeID):
    route = traci.route.getEdges(routeID)
    return route


#Possible Extra Getters
#getRoadID => Value of the current lane the vehicle is at

#Setters (Actuators)

#Traffic Lights  ----------------------------------------------------------------
def setLightState(lightID,state):
    traci.trafficlight.setRedYellowGreenState(lightID,state)
    #Example : setLightState( "c" ,"GrGGGG")
    #Sets the named tl's state as a tuple of light definitions from
    #rugGyYuoO, for red, red-yellow, green, yellow, off, where
    #lower case letters mean that the stream has to decelerate.

#Vehicles--------------------------------------------------------------------------------
def changeLane(vehID,laneID,duration):
    traci.vehicle.changeLane(vehID, laneID, duration)
    #changeLane(string,int,double) -> None
    #Forces a lane change to the lane with the given index; if successful,
    #the lane will be chosen for the given amount of time (in s).


#Optional
def changeSublane(vehID,latDist):
    traci.vehicle.changeSublane(vehID, latDist)
    #changeLane(string, double) -> None
    #changeSublane("0ev",-1)
    #Forces a lateral change by the given amount
    #(negative values indicate changing to the right, positive to the left).
    #This will override any other lane change motivations but conform to
    #safety-constraints as configured by laneChangeMode.



# Routes--------------------------------------------------------------------------------
def setRoute(vehID,edgeList):
    traci.vehicle.setRoute(vehID, edgeList)
    #setRoute(string, list) ->  None
    #changes the vehicle route to given edges list.
    #The first edge in the list has to be the one that the vehicle is at at the moment.
    #example usage:
    #setRoute('1', ['1', '2', '4', '6', '7'])
    #this changes route for vehicle id 1 to edges 1-2-4-6-7



#setRouteID(self, vehID, routeID)
#setRouteID(string, string) -> None
#Changes the vehicles route to the route with the given id.
#-----Check if we are using IDs for the routes

#Optional------------------------------------------------------------------------------
def setRoutingMode(vehID,routingMode):
    traci.vehicle.setRoutingMode(vehID, routingMode)
    #sets the current routing mode:
    #tc.ROUTING_MODE_DEFAULT    : use weight storages and fall-back to edge speeds (default)
    #tc.ROUTING_MODE_AGGREGATED : use global smoothed travel times from device.rerouting
#--------------------------------------------------------------------------------------




## AGENT RELATED CODE

def getLightID(road):
    if road == 'ab':
        lightID = 'b'
    elif road == 'bc':
        lightID = 'c'
    elif road == 'cd':
        lightID = 'd'
    elif road == 'de':
        lightID = 'e'
    elif road == 'ce':
        lightID = 'e'
    elif road == 'ea':
        lightID = 'a'
    elif road == 'ed':
        lightID = 'd'
    elif road == 'da':
        lightID = 'a'
    elif road == 'eb':
        lightID = 'b'
    elif road == 'ba':
        lightID = 'a'
    elif road == 'ad':
        lightID = 'd'
    elif road == 'dc':
        lightID = 'c'
    elif road == 'cb':
        lightID = 'b'
    elif road == 'be':
        lightID = 'e'
    elif road == 'ae':
        lightID = 'e'
    elif road == 'de':
        lightID = 'e'
    elif road == 'ec':
        lightID = 'c'
    elif road == 'be':
        lightID = 'e'
    else:
    #    print('Nothins')
        return
    #lights = getLightState(lightID)
        #print('nada man')
        return
    return lightID

##here we need to write the code for the agent.

def checkLightStatus(lightID):
    lights = getLightState(lightID)
    return lights

def EmergncyAgent(emPos):
    #gets current road of emergency vehicle
    lightState = checkCurrentLights(emPos)
    num_vehs = getNumberOfVehicles(emPos + '_0')
    # if lightState != None:
    #     print(lightState)
    #     print(lightState[0])
    #     print(lightState[1])
    #     print(lightState[2])
    #     if lightState[0] == 'G':
    #         setLightState('b','GGrrGG')
    #         print('hellowworld')


    return lightState, num_vehs

def Priority(lane):
    mylane = lane[:2]
    if checkCurrentLights(mylane) != None:
        lightID = checkCurrentLights(mylane)
        free_lane_pos = traci.vehicle.getLanePosition("0ev") / traci.lane.getLength(lane)
        
        if traci.lane.getWaitingTime(lane) >= 0.1 or free_lane_pos >= 0.5:
            last_traffic = traci.trafficlight.getPhase(lightID)
            print(last_traffic)
            mylight = ""
            for i in traci.trafficlight.getControlledLanes(lightID):
                if i == lane:
                    mylight += "G"
                else:
                     mylight += "r"
            print (mylight)
            setLightState(lightID,mylight)

def getLastPhase(lightID):
    if lightID == None:
        return
    else:
        last = traci.trafficlight.getPhase(lightID)
        return last

def getPhaseName(lights):
    if lights == None:
        return
    else:
        phasename = traci.trafficlight.getPhaseName(lights)
        return phasename

def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_bc")
        emPos = getEmPos()
        lights = getLightID(emPos)
        #print('em pos is ', emPos)
        #print(EmergncyAgent(emPos))

        #print(num_vehs)
        #print(getRoute('route_0'))

        #print(getEmPos())
        #print("vehicles on bc_0 is ", no_vehs)
        
        for veh in det_vehs:
            if veh == "0ev":
                print(veh)
                #traci.vehicle.changeTarget("0ev", "ce")
                #print(veh)
                traci.vehicle.changeTarget("0ev", "ce")
                lane = traci.vehicle.getLaneID("0ev")
                #print(getNumberOfVehicles(lane))

        
                #print(traci.lane.getWaitingTime("bc_0"))
                #setLightState("c","rrrrrr")
                #setLightState("d","rrrrrr")
                #print(traci.simulation.getCurrentTime())
            #setLightState("c","rrrrrr")
        #print(traci.vehicle.getMinGapLat("0ev"))
        #if traci.simulation.getCurrentTime() == 23000:
            #print(traci.lane.getTraveltime("bc_0"))
            #print(traci.lane.getWaitingTime("bc_0"))
            #setLightState("c","rrrrGG")


        lane = traci.vehicle.getLaneID("0ev")
        Priority(lane)
        #print(traci.vehicle.getRoadID("0ev"))
        '''
        if traci.lane.getWaitingTime(lane) >= 0.1:
            #print(lane)
            if lane == "bc_0":
                #print(traci.trafficlight.getControlledLanes("c"))
                #print(traci.trafficlight.getControlledLanes("c").index("bc_0"))
                last_traffic = traci.trafficlight.getPhase("c")
                #print(last_traffic)
                mylight = ""
                for i in traci.trafficlight.getControlledLanes("c"):
                    if i == lane:
                        mylight += "G"
                    else:
                        mylight += "r"
                #print (mylight)
                setLightState("c",mylight)
            if lane == "ce_0":
                #setLightState("c",last_traffic)
                traci.vehicle.changeTarget("0ev", "ed")
                setLightState("e", "rrrGGGrrrrrrr")
            if lane == "ed_0":
                traci.vehicle.changeTarget("0ev", "da")
                setLightState("d", "GGrrrr")

       '''
        #if step == 100:
        #    traci.vehicle.changeTarget("1", "de")
        #    traci.vehicle.changeTarget("3", "de")

        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "network.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
