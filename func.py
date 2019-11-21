#!/usr/bin/env python

import os
import sys
import optparse
import subprocess
import random
import time
import network
from network import traci

class functions:
    # # we need to import some python modules from the $SUMO_HOME/tools directory
    # if 'SUMO_HOME' in os.environ:
    #     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    #     sys.path.append(tools)
    # else:
    #     sys.exit("please declare environment variable 'SUMO_HOME'")
    #
    # sys.path.append('/home/jonny-smyth/Desktop/sumo/tools')
    #
    # #chesare9000
    # #MAC -> export SUMO_HOME="/usr/local/opt/sumo/share/sumo
    # #UBT -> sys.path.append('/home/chesare9000/Documents/MAS/1.Traffic/sumo/tools')
    #
    # from sumolib import checkBinary  # Checks for the binary in environ vars
    # import traci
    #
    # # Getters (Sensors)
    #
    # def get_options():
    #     opt_parser = optparse.OptionParser()
    #     opt_parser.add_option("--nogui", action="store_true",
    #                          default=False, help="run the commandline version of sumo")
    #     options, args = opt_parser.parse_args()
    #     return options

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
            return
        return lightID

    ##here we need to write the code for the agent.

    def checkLightStatus(lightID):
        lights = getLightState(lightID)
        return lights

    def startTimer():
        t0 = time.time()
        return t0

    def stopTimer():
        t1 = time.time()
        return t1


    ## AGENT RELATED CODE

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
    # some global vars
    '''
    def Priority(lane):
        global last_light
        global last_phase
        global first_time
        # string proccesing to get lightID
        mylane = lane[:2]

        if getLightID(mylane) != None:
            lightID = getLightID(mylane)



            # if we are in  first simulation step just store first traffic light and
            # and traffic light phase as last ones
            if first_time == 0:
                print('first time')
                last_light = lightID
                last_phase = getLastPhase(last_light)
                print(last_phase)
                first_time = first_time = 1

            # otherwise if changed lane, so we changed also traffic light
            # we try to change the previous light to last light phase before the
            # emergency hack
            elif last_light != "" and last_light != lightID:
                print(getLastPhase(last_light))
                setLightPhase(last_light,last_phase)
                print
                last_light = lightID
                last_phase = getLastPhase(last_light)


            # we just get the position of car in lane
            free_lane_pos = traci.vehicle.getLanePosition("0ev") / traci.lane.getLength(lane)

            # if car's waiting is going to increase or lane is empty and
            # we are approaching the last 30% of lane, make the lane's light green
            if traci.lane.getWaitingTime(lane) >= 0.1 or free_lane_pos >= 0.65:

                # we change to green only lights of the lane that the ev is
                mylight = ""
                for i in traci.trafficlight.getControlledLanes(lightID):
                    if i == lane:
                        mylight += "G"
                    else:
                         mylight += "r"
                setLightState(lightID,mylight)
    '''

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

    def setLightPhase(lightID,phase):
        traci.trafficlight.setPhase(lightID,phase)

    def setProgram(lightID):
        if lightID == "a":
            traci.trafficlight.setProgram(lightID,'0')
        if lightID == "b":
            traci.trafficlight.setProgram(lightID,'1')
        if lightID == "c":
            traci.trafficlight.setProgram(lightID,'2')
        if lightID == "d":
            traci.trafficlight.setProgram(lightID,'3')
        if lightID == "e":
            traci.trafficlight.setProgram(lightID,'4')

#Manage the Ambulance Behaviour

def closeLane(laneID):
    traci.lane.setDisallowed(str(laneID),["emergency"])
    print("Lane " + str(laneID) + " closed for the ambulance")

def updateEvRoute(finalLane):
    traci.vehicle.changeTarget("0ev",finalLane )
    print("Updating goal to corner " + finalLane)
    print("Modified Route: " + str(traci.vehicle.getRoute("0ev")))

def getLaneTraffic(laneID):
    laneInfo = traci.lane.getLastStepVehicleNumber(laneID)
    print("Traffic on the Lane " + str(laneID) + " : " + str(laneInfo))
    return laneInfo


#Comparing the Traffic on both adjacent lanes
#The one with more traffic will be closed
#If there is no traffic both remain open

def compare(laneToCompare,initialRoute):

    links = traci.lane.getLinks(laneToCompare,False)

    if len(links) == 2 :

        first_lane= list(links[0])[0]
        second_lane = list(links[1])[0]

        print("Lane with " + str(len(links)) + " Junctions : "
        + str(first_lane)+ " and " + str(second_lane))

        first_lane_traffic  = getLaneTraffic(first_lane)
        second_lane_traffic = getLaneTraffic(second_lane)

        if first_lane_traffic > second_lane_traffic:
            closeLane(first_lane)
            updateEvRoute(str(initialRoute[-1]))

        elif second_lane_traffic > first_lane_traffic:
            closeLane(second_lane)
            updateEvRoute(str(initialRoute[-1]))

        else: print("No lane will be closed")

    elif len(links) == 3:

        first_lane  =  list(links[0])[0]
        second_lane =  list(links[1])[0]
        third_lane  =  list(links[2])[0]

        print("Lane with " + str(len(links)) + " Junctions : "
        + str(first_lane)  + " , " + str(second_lane) + " and " + str(third_lane))

        first_lane_traffic  = getLaneTraffic(first_lane)
        second_lane_traffic = getLaneTraffic(second_lane)
        third_lane_traffic  = getLaneTraffic(third_lane)

        if first_lane_traffic > second_lane_traffic and first_lane_traffic > third_lane_traffic :
            closeLane(first_lane)

        elif second_lane_traffic > first_lane_traffic and second_lane_traffic > third_lane_traffic:
            closeLane(second_lane)

        elif third_lane_traffic > first_lane_traffic and third_lane_traffic > second_lane_traffic:
            closeLane(third_lane)

        else : print("No lane will be closed")

        updateEvRoute(str(initialRoute[-1]))        
