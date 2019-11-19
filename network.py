#!/usr/bin/env python

import os
import sys
import optparse
import subprocess
import random
import time
from func import mas


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

class RoadAgent:
    def __init__(self, id):
        self.id = id

    def begin(self, id):
        global num_cars_on_road
        global cars_ab_0
        num_cars_on_road =  no_vehs = traci.lane.getLastStepVehicleNumber(id)


def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        road1.begin('ab_0')
        print(num_cars_on_road)
        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()
    first_time = 0
    road1 = RoadAgent('ab_0')
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "network.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
