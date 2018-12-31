#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Primoz Zajec
# @date    2018-11-
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

import paho.mqtt.client as mqtt
import time
import json

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

global state
state = [""]
global dataJson

def run():
    global mqttClient
    global traci
    global state
    global carName
    carName = ""
    """execute the TraCI control loop"""
    step = 0

# TAXI 1 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("279297476","279297476").edges
    print("route:::: ", route)
    traci.route.add("taxi1Start", route)
    traci.vehicle.add('taxi1', "taxi1Start")
    traci.vehicle.setColor('taxi1', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi1", "279297476", 5.0, flags=traci.constants.STOP_PARKING)

# TAXI 2 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("-167299074#1","66478404#2").edges
    traci.route.add("taxi2Start", route)
    traci.vehicle.add('taxi2', "taxi2Start")
    traci.vehicle.setColor('taxi2', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi2", "-167299074#1", 5.0, flags=traci.constants.STOP_PARKING)

# TAXI 3 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("270055655","66478404#2").edges
    traci.route.add("taxi3Start", route)
    traci.vehicle.add('taxi3', "taxi3Start")
    traci.vehicle.setColor('taxi3', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi3", "270055655", 5.0, flags=traci.constants.STOP_PARKING)


    
    cars = []

    while traci.simulation.getMinExpectedNumber() > 0:
#    while step < 1000:
        traci.simulationStep()
#        print(step)
        vehs = traci.vehicle.getIDList()
#        print(vehs)
        pos = {}
#        for v in vehs:
#        for name in ["taxi1"]:#, "taxi2", "taxi3"]:
        if (carName != ""):
            pos2D = traci.vehicle.getPosition(carName)
            pos[carName] = traci.simulation.convertGeo(pos2D[0], pos2D[1])
            #convertRoad(self, x, y, isGeo=False)
            topic = "pos/slovenia/ljubljana"
            payload = json.dumps({"id":carName, "lon":pos[carName][0], "lat":pos[carName][1]})
            

#            edgeIDt1 = traci.simulation.convertRoad(14.48367, 46.04032, True)
#            print("::::::: ", edgeIDt1)
#            edgeIDt2 = traci.simulation.convertRoad(14.48507, 46.04064, True)
#            print("::::::: ", edgeIDt2)
#            edgeIDt3 = traci.simulation.convertRoad(14.49044, 46.04335, True)
#            print("::::::: ", edgeIDt3)
##            traci.vehicle.getAdaptedTraveltime("taxi1", time, edgeID)
#            print("traveltime", traci.vehicle.getAdaptedTraveltime("taxi1", 0, edgeIDt1[0]))
#            print("traveltime", traci.vehicle.getAdaptedTraveltime("taxi1", 0, edgeIDt2[0]))
#            print("adaptedTraveltime after adaption in interval (check time 0)", traci.edge.getTraveltime(edgeIDt1[0]))
#            print("adaptedTraveltime after adaption in interval (check time 0)", traci.edge.getTraveltime(edgeIDt2[0]))
#            print("adaptedTraveltime after adaption in interval (check time 0)", traci.edge.getTraveltime(edgeIDt3[0]))
#
#            route1 = traci.simulation.findRoute("279297476",edgeIDt1[0]).edges
#            route2 = traci.simulation.findRoute("279297476",edgeIDt2[0]).edges
#            print("kkkkk: ",route)
#            time = 0
#            for edge in route1 :
#               time += traci.edge.getTraveltime(edge)
#            print("time111: ",time)
#            time = 0
#            for edge in route2 :
#               time += traci.edge.getTraveltime(edge)
#            print("time2222: ",time)




#           print("convertGeo2D", traci.simulation.convertGeo(pos["taxi1"][0], pos["taxi1"][1], True))
#            print("------------")
#            print(payload)
            if(step%1 == 0):
                mqttClient.publish(topic, payload)
#            print(pos[v])
#        print(vehs)
#        if step == 40:
        if state[0] == "request":
            state_ = state
            state = [""]
            stateAction(state_)
        if state[0] == "requestSpecific":
            state_ = state
            state = [""]
            stateAction(state_)

##            for veh in ["taxi1"]:#, "taxi2", "taxi3"]:
# 
#            print("----------------------------------")
#            print("We are in 40s")
#            print("----------------------------------")
##            if traci.vehicle.getSpeed("right_0") == 0:
##                traci.vehicle.resume("right_0")
#            # changeTarget(vehicleID, edgeID) - can make turns
##            traci.vehicle.changeTarget("right_0", "04")
#            # setRoute(self, vehID, edgeList) ex:setRoute('1', ['1', '2', '4'])
##            traci.vehicle.setRoute("right_0", ["10", "03", "30"])
#            # setRouteID(self, vehID, routeID)
##            traci.vehicle.setRouteID("right_0", "down")
##            newRoute = traci.simulation.findRoute("279297476", "39726119#0").edges
##            edgeID = traci.simulation.convertRoad(14.49634, 46.04794, True)
##            edgeID = traci.simulation.convertRoad(14.49278, 46.04561, True)
#            edgeID = traci.simulation.convertRoad(14.47917, 46.04494, True)
##            newRoute = traci.simulation.findRoute("279297476", edgeID[0]).edges
#            currentEdge = traci.vehicle.getRoadID("taxi1")
#            print("ROAD:::", currentEdge)
###            newRoute = traci.simulation.findRoute(currentEdge, "66478404#2").edges
#            newRoute = traci.simulation.findRoute(currentEdge, edgeID[0]).edges
#            print("nova rutaaaaa: ", newRoute)
#            traci.vehicle.setRoute("taxi1", newRoute)
#            traci.vehicle.setStop("taxi1", edgeID[0], flags=traci.constants.STOP_PARKING)
####            traci.vehicle.setStop("taxi1", "66478404#2", flags=traci.constants.STOP_PARKING)
#            if traci.vehicle.getSpeed("taxi1") == 0:
#                traci.vehicle.resume("taxi1")
        step += 1
    mqttClient.disconnect()
    mqttClient.loop_stop()
    traci.close()
    sys.stdout.flush()

# states that comes from mqttOnMessage
def stateAction(state):
    global dataJson
    ######################   REQUEST FOR ALL (DURATION)   ###################
    if(state[0] == "request"):
        appEdgeID = traci.simulation.convertRoad(dataJson["appLon"], dataJson["appLat"], True)
        destEdgeID = traci.simulation.convertRoad(dataJson["destLon"], dataJson["destLat"], True)
        route2 = traci.simulation.findRoute(appEdgeID[0],destEdgeID[0]).edges
        route2time = 0
        for edge in route2 :
           route2time += traci.edge.getTraveltime(edge)

        for car in ["taxi1", "taxi2", "taxi3"]:
            print("For the vehicle :{}".format(car))
            vehEdgeID = traci.vehicle.getRoadID(car)
#            print("VehEdgeID :", vehEdgeID)
            route1 = traci.simulation.findRoute(vehEdgeID,appEdgeID[0]).edges
#            print("Route1 :", route1)
            route1time = 0
            for edge in route1 :
                mtime = traci.edge.getTraveltime(edge)
                if (mtime > 40.0):
                    print("STRANGE EST. TIME FOR NODE: {}!!!!!!!!!!!!!!!!!!!!!!!!!!".format(edge))
                    mtime = 0.0
                route1time += mtime
            duration = route1time + route2time
            minutes = int(duration / 60)
            seconds = int(duration % 60)
            print("minutes: ", minutes)
            print("seconds: ", seconds)

            topic = "res/" + dataJson["id"] + "/duration"
            payload = json.dumps({"name":car, "duration": {"minutes":minutes, "seconds":seconds}})
            mqttClient.publish(topic,payload)

    ########################   SPECIFIC TRIP REQUEST   #################
    if(state[0] == "requestSpecific"):
        global carName
        carName = state[1]
        appEdgeID = traci.simulation.convertRoad(dataJson["appLon"], dataJson["appLat"], True)
        print("appEdgeID :", appEdgeID)
        destEdgeID = traci.simulation.convertRoad(dataJson["destLon"], dataJson["destLat"], True)
        print("destEdgeID :", destEdgeID)
        route2 = traci.simulation.findRoute(appEdgeID[0],destEdgeID[0]).edges

        print("For the vehicle :{}".format(state[1]))
        vehEdgeID = traci.vehicle.getRoadID(state[1])
        print("vehEdgeID :", vehEdgeID)
        route1 = traci.simulation.findRoute(vehEdgeID,appEdgeID[0]).edges
        print("route1 :", route1)

        #getDistanceRoad(self, edgeID1, pos1, edgeID2, pos2, isDriving=False)
        distance1 = traci.simulation.getDistanceRoad(vehEdgeID, 0, appEdgeID[0], 0, isDriving=True)
        distance2 = traci.simulation.getDistanceRoad(appEdgeID[0], 0, destEdgeID[0], 0, isDriving=True)
        print("-AAA--a-a-a--a-a-a--a")
        print(distance1)
        print(distance2)

        if traci.vehicle.getSpeed(state[1]) == 0:
            traci.vehicle.setRoute(state[1], route1)
            traci.vehicle.setStop(state[1], appEdgeID[0], flags=traci.constants.STOP_PARKING)
            traci.vehicle.resume(state[1])


def getOptions():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def mqttOnConnect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#    client.subscribe("req/slovenia/#")
    client.subscribe("req/#")
    print("Subscribed")

# The callback for when a PUBLISH message is received from the server.
def mqttOnMessage(client, userdata, msg):
    global traci
    global state
    global dataJson
    try:
        dataJson = json.loads(msg.payload.decode("utf-8"))
    except Exception as e:
        print(e)
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    if msg.topic == "req/slovenia/ljubljana":
        state = ["request"]
    splitTopic = msg.topic.split("/")
    print(splitTopic)
    if ( splitTopic[0] == "req" and splitTopic[1] in ["taxi1", "taxi2", "taxi3"]):
        state = ["requestSpecific", splitTopic[1]]
#        for v in vehs:
#        for veh in ["taxi1"]:#, "taxi2", "taxi3"]:
#            pos2D = traci.vehicle.getPosition("taxi1")
#            print("POSSSS:",pos2D)
#            print("bbbbbbbbbbbbbbbb")
#            vehEdgeID = traci.vehicle.getRoadID("taxi1")
#            print("VEssssssss:",vehEdgeID)
#            topic = "pos/slovenia/ljubljana"
#            payload = json.dumps({"id":veh, "lon":pos[veh][0], "lat":pos[veh][1]})

    print("---------------------------------")
    print("MQTT message:")
    print("Topic: " + msg.topic)
    print("payload: " + msg.payload)
#    if traci.vehicle.getSpeed("right_0") == 0:
#        traci.vehicle.resume("right_0")
#    traci.vehicle.setRoute("right_0", ["10", "03", "30"])
#    traci.vehicle.setStop("right_0", "30", 400.0, flags=traci.constants.STOP_PARKING)


def main():
    global mqttClient
    mqttClient = mqtt.Client("mobiClient")
    mqttClient.on_connect = mqttOnConnect
    mqttClient.on_message = mqttOnMessage

    mqttClient.connect("178.62.252.50", port=1883, keepalive=60)

    # Loop forever
    try:
#        mqttClient.loop_forever()
        mqttClient.loop_start()
        run()


    # Catches SigINT
    except KeyboardInterrupt:
        mqttClient.disconnect()
        print("Exiting main thread")
        time.sleep(2.0)



# this is the main entry point of this script
if __name__ == "__main__":
    options = getOptions()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
#    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    global traci
    traci.start([sumoBinary, "-c", "data/cross.sumocfg", "--collision.check-junctions","true","--collision.action","teleport"])
#    run()
    main()
