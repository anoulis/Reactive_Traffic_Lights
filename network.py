#!/usr/bin/env python

import os
import sys
import optparse
import subprocess
import random
import time
import func
import trafficLightsAgent
import emergencyVehicle
import trafficControl
import lanesAgent

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

def Priority(ev):
    #print(lanes_dict.get(ev.getLane()))
    current_lane_agent = lanes_dict.get(ev.getLane())

    current_tl_agent = tl_dict.get(func.functions.getLightID(current_lane_agent.getID()))
    free_lane_pos = ev.getPosition() /  current_lane_agent.getLaneLength()
    # if car's waiting is going to increase or lane is empty and
    # we are approaching the last 30% of lane, make the lane's light green
    if current_lane_agent.getLaneWaitingTime() >= 0.1 or free_lane_pos >= 0.65:
        # we change to green only lights of the lane that the ev is
        mylight = ""
        for i in current_tl_agent.getControlledLanes():
            if i == current_lane_agent.getID():
                mylight += "G"
            else:
                mylight += "r"
        current_tl_agent.setCustomLights(mylight)
    return


def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        Priority(ev)
        #functions.Priority()
        print(lanes_dict.get(ev.getLane()).getID())
        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()
    first_time = 0
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "network.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
                
   
    functions = func.functions 
    tlAgent = trafficLightsAgent.TrafficLightAgent

    evAgent = emergencyVehicle.EmergencyVehicle
    ev = evAgent("0ev")

    lanesAgent = lanesAgent.LanesAgent

    #tl_list = []
    tl_dict= {}
    lanes_dict = {}
    lanes_dict["ac"] = lanesAgent("ac")
    for k in traci.lane.getIDList()[42:]:
        temp = k[:2]
        lanes_dict[str(temp)] = lanesAgent(str(temp))
    
    for i in functions.getAllLightIds():
       # tl_list.append( tlAgent(str(i)))
        tl_dict[str(i)] = tlAgent(str(i))
    run()
