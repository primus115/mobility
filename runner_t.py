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
import threading

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

class myThread(threading.Thread):

    def __init__(self, threadID):
        print("Thread initialized!")
        sys.stdout.flush()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.end = False

    def run(self):
        print("Thread started!")
        sys.stdout.flush()
        mobi()
        print("Thread ended!")
        sys.stdout.flush()

    def stop(self):
        self.end = True

def mobi():
    global message
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("0", 2)
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("right_0", "10", 50.0, flags=traci.constants.STOP_PARKING)
    traci.vehicle.setStop("left_0", "20", 50.0, flags=traci.constants.STOP_PARKING)
    while traci.simulation.getMinExpectedNumber() > 0:
#    while step < 1000:
        traci.simulationStep()
        print(step)
        sys.stdout.flush()
#        if traci.trafficlight.getPhase("0") == 2:
#            # we are not already switching
#            if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
#                # there is a vehicle from the north, switch
#                traci.trafficlight.setPhase("0", 3)
#            else:
#                # otherwise try to keep green for EW
#                traci.trafficlight.setPhase("0", 2)
##        vehList = traci.getIDList()
#        vehs = traci.vehicle.getIDList()
#        pos = {}
#        for v in vehs:
#            pos[v] = traci.vehicle.getPosition(v)
#            print(pos[v])
#        print(vehs)
#        if message != "":
#            print(message)
#            message = ""
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
        step += 1
    mqttClient.disconnect()
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
    sys.stdout.flush()

    client.subscribe("data/#")
    print("Subscribed")
    sys.stdout.flush()

# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    global message
    m_decode=str(msg.payload.decode("utf-8","ignore"))
#    if msg.topic == "sigfox/survey":
#    if msg.payload == "EXIT":
#    print("Topic: " + msg.topic)
#    print("payload: " + msg.payload)
#    speed = (traci.vehicle.getSpeed("right_0"))
    message = "aaaaaaaaaaaaaaaa"
    print("+++++++++++++++++++++++++++++++++++++++++++++")
#    if traci.vehicle.getSpeed("right_0") == 0:
#        traci.vehicle.resume("right_0")
#    traci.vehicle.setRoute("right_0", ["10", "03", "30"])
#    traci.vehicle.setStop("right_0", "30", 400.0, flags=traci.constants.STOP_PARKING)




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
    traci.start([sumoBinary, "-c", "data/cross.sumocfg"])

    try:
        mqttClient = mqtt.Client("mobiClient")
        mqttClient.on_connect = mqtt_on_connect
        mqttClient.on_message = mqtt_on_message
        mqttClient.connect("localhost")

        t1 = myThread(1)
        t1.start()
        mqttClient.loop_forever();

    # Catches SigINT
    except KeyboardInterrupt:
        t1.stop()
        mqttClient.disconnect()
        traci.close()
        sys.stdout.flush()
        print("Exiting main thread")
        time.sleep(2.0)


