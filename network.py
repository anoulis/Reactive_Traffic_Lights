
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
import detectorAgent

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

def run():
    step = 0
    oldLaneStatus=0
    global initialRoute

    initialRoute = traci.vehicle.getRoute("0ev")
    print("Initial Route: " + str(initialRoute))
    traci.vehicle.changeTarget("0ev", str(initialRoute[-1]))
    print("Modified Route: " + str(traci.vehicle.getRoute("0ev")))

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        updatedlaneStatus = traci.vehicle.getRoadID("0ev")

        if updatedlaneStatus != oldLaneStatus:
            func.compare(updatedlaneStatus+"_0", initialRoute)
            oldLaneStatus=updatedlaneStatus
        #func.updateEvRoute(str(initialRoute[-1])) Testing , not to impl.

        #Priority(ev)
        trafficControl.Priority(ev,lanes_dict,tl_dict,det_dict)
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

    myfunctions = func.functions
    evAgent = emergencyVehicle.EmergencyVehicle
    lanesAgent = lanesAgent.LanesAgent
    tlAgent = trafficLightsAgent.TrafficLightAgent
    detectorAgent = detectorAgent.DetectorAgent

    det_dict = {}
    tl_dict= {}
    lanes_dict = {}

    ev = evAgent("0ev")
    lanes_dict["ac"] = lanesAgent("ac")
    det_dict["ac"] = detectorAgent("ac")
    for k in traci.lane.getIDList()[42:]:
        temp = k[:2]
        lanes_dict[str(temp)] = lanesAgent(str(temp))
        det_dict[str(temp)] = detectorAgent(str(temp))

    for i in myfunctions.getAllLightIds():
       # tl_list.append( tlAgent(str(i)))
        tl_dict[str(i)] = tlAgent(str(i))
    run()
