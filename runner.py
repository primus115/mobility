#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
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

global message
message = ""

def run():
    global mqttClient
    global traci
    global message
    """execute the TraCI control loop"""
    step = 0

    route = traci.simulation.findRoute("3314142#3","3314142#4").edges
    traci.route.add("taxi1Start", route)
    traci.vehicle.add('taxi1', "taxi1Start")
    traci.vehicle.setColor('taxi1', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi1", "3314142#3", 5.0, flags=traci.constants.STOP_PARKING)

    while traci.simulation.getMinExpectedNumber() > 0:
#    while step < 1000:
        traci.simulationStep()
        print(step)
        vehs = traci.vehicle.getIDList()
#        print(vehs)
        pos = {}
#        for v in vehs:
        pos2D = traci.vehicle.getPosition("taxi1")
        pos["taxi1"] = traci.simulation.convertGeo(pos2D[0], pos2D[1])
#        topic = "pos/sloveni/ljubljana/" + v
        topic = "pos/sloveni/ljubljana/taxi1"
        payload = json.dumps({"id":"taxi1", "lon":pos["taxi1"][0], "lat":pos["taxi1"][1]})

#        print("convertGeo2D", traci.simulation.convertGeo(pos["taxi1"][0], pos["taxi1"][1], True))
        print("------------")
        print(payload)
        if(step%1 == 0):
            print("nottttttttttttttttttttttttt")
            mqttClient.publish(topic, payload)
#            print(pos[v])
#        print(vehs)
#        if step == 40:
        if message != "":
            message = ""
            print("----------------------------------")
            print("We are in 40s")
            print("----------------------------------")
#            if traci.vehicle.getSpeed("right_0") == 0:
#                traci.vehicle.resume("right_0")
            # changeTarget(vehicleID, edgeID) - can make turns
#            traci.vehicle.changeTarget("right_0", "04")
            # setRoute(self, vehID, edgeList) ex:setRoute('1', ['1', '2', '4'])
#            traci.vehicle.setRoute("right_0", ["10", "03", "30"])
            # setRouteID(self, vehID, routeID)
#            traci.vehicle.setRouteID("right_0", "down")
            if traci.vehicle.getSpeed("taxi1") == 0:
                traci.vehicle.resume("taxi1")
            newRoute = traci.simulation.findRoute("3314142#3", "72267225").edges
            traci.vehicle.setRoute("taxi1", newRoute)
        step += 1
    mqttClient.disconnect()
    mqttClient.loop_stop()
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("data/#")
    print("Subscribed")

# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    global traci
    global message
    message = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    m_decode=str(msg.payload.decode("utf-8","ignore"))
#    if msg.topic == "sigfox/survey":
#    if msg.payload == "EXIT":
    print("Topic: " + msg.topic)
    print("payload: " + msg.payload)
#    if traci.vehicle.getSpeed("right_0") == 0:
#        traci.vehicle.resume("right_0")
#    traci.vehicle.setRoute("right_0", ["10", "03", "30"])
#    traci.vehicle.setStop("right_0", "30", 400.0, flags=traci.constants.STOP_PARKING)


def main():
    global mqttClient
    mqttClient = mqtt.Client("mobiClient")
    mqttClient.on_connect = mqtt_on_connect
    mqttClient.on_message = mqtt_on_message

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
    options = get_options()

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
    traci.start([sumoBinary, "-c", "data/cross.sumocfg"])
#    run()
    main()
