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
from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        #print(step)
        no_vehs = traci.lane.getLastStepVehicleNumber("bc_0")
        det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        print(no_vehs)
        for veh in det_vehs:
            if veh == "0ev":
                print(veh)
                traci.vehicle.changeTarget("0ev", "ce")
                traci.trafficlight.setRedYellowGreenState("c", "rrrrGG")

        if step == 100:
            traci.vehicle.changeTarget("1", "de")
            traci.vehicle.changeTarget("3", "de")

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
