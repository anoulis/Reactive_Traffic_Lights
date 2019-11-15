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

#sys.path.append('/home/jonny-smyth/Desktop/sumo/tools')
#sys.path.append('/home/chesare9000/Documents/MAS/1.Traffic/sumo/tools')

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


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


#Possible Getters
#getRoadID => Value of the current lane the vehicle is at


#Setters

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

# contains TraCI control loop

def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_bc")
        #emPos = getEmPos()
        #print(emPos)
        #num_vehs = getNumberOfVehicles(emPos + '_0')
        #print(num_vehs)

        if step==0:
            print(getRoute('route_0'))

        elif step==10:
            lastRoad = traci.vehicle.getRoadID("0ev")
            setRoute("0ev", [lastRoad,'bc','ce'])

            print(lastRoad)
            #traci.vehicle.changeTarget("0ev", "dc")
        #print(getEmPos())
        #print("vehicles on bc_0 is ", no_vehs)

        #if step == 100:
            #traci.vehicle.changeTarget("1", "de")
            #traci.vehicle.changeTarget("3", "de")

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
