import trafficLightsAgent
from trafficLightsAgent import TrafficLightAgent
from emergencyVehicle import EmergencyVehicle
from lanesAgent import LanesAgent
import network 
import func

global lanes_dict,tl_dict
lanes_dict = {}
tl_dict = {}
def Priority(ev):
    print(lanes_dict.get(ev.getLane()))
    current_lane_agent = lanes_dict.get(ev.getLane())
    print(current_lane_agent)

    current_tl_agent = tl_dict.get(func.functions.getLightID(current_lane_agent))
    free_lane_pos = ev.getPosition /  current_lane_agent.getLaneLength()
    # if car's waiting is going to increase or lane is empty and
    # we are approaching the last 30% of lane, make the lane's light green
    if current_lane_agent.getLaneWaitingTime() >= 0.1 or free_lane_pos >= 0.65:
        # we change to green only lights of the lane that the ev is
        mylight = ""
        for i in current_tl_agent.getControlledLanes():
            if i == current_lane_agent:
                mylight += "G"
            else:
                mylight += "r"
        current_tl_agent.setLightState(mylight)
    return




