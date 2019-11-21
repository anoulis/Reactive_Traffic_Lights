import network 
import func

global last_line
last_line=""
def Priority(ev,lanes_dict,tl_dict,det_dict ):
    if (lanes_dict.get(ev.getLane()) != None):
        global last_line
        current_lane_agent = lanes_dict.get(ev.getLane())
        current_det_agent = det_dict.get(ev.getLane())
        current_tl_agent = tl_dict.get(func.functions.getLightID(current_lane_agent.getID()))

        # restore lights program
        if(current_det_agent.isEmergencyVehicleHere()):
            temp  = tl_dict.get(func.functions.getLightID(last_line)).getID()
            func.functions.setProgram(temp)
    
        free_lane_pos = ev.getPosition() /  current_lane_agent.getLaneLength()
        # if car's waiting is going to increase or lane is empty and
        # we are approaching the last 30% of lane, make the lane's light green
        if current_lane_agent.getLaneWaitingTime() >= 0.1 or free_lane_pos >= 0.65:

            # we change to green only lights of the lane that the ev is
            mylight = ""
            for i in current_tl_agent.getControlledLanes():
                if i == current_lane_agent.getFixedID():
                    mylight += "G"
                else:
                    mylight += "r"
            current_tl_agent.setCustomLights(mylight)
            last_line = current_lane_agent.getID()
    
    return






