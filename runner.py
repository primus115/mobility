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
# @date    2018-11-17
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
from threading import Thread

from web3 import Web3, HTTPProvider
from getpass import getpass  

RINKEBY = "https://rinkeby.infura.io/v3/23d1d5956dc54a068ab6887ef8e711b3"
#ETHER_PER_METER = 0.00001
METER_PER_ETHER = 100000

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

def run():
    global mqttClient
    global state
    global carName
    carName = ""
    """execute the TraCI control loop"""
    step = 0
    step_ = 0
    stopCount = 0

# TAXI 1 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("279297476","279297476").edges
    traci.route.add("taxi1Start", route)
    traci.vehicle.add('taxi1', "taxi1Start")
    traci.vehicle.setColor('taxi1', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi1", "279297476", flags=traci.constants.STOP_PARKING)

# TAXI 2 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("-167299074#1","66478404#2").edges
    traci.route.add("taxi2Start", route)
    traci.vehicle.add('taxi2', "taxi2Start")
    traci.vehicle.setColor('taxi2', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi2", "-167299074#1", flags=traci.constants.STOP_PARKING)

# TAXI 3 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("270055655","66478404#2").edges
    traci.route.add("taxi3Start", route)
    traci.vehicle.add('taxi3', "taxi3Start")
    traci.vehicle.setColor('taxi3', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi3", "270055655", flags=traci.constants.STOP_PARKING)
    
    cars = []

    while traci.simulation.getMinExpectedNumber() > 0:
#    while step < 1000:
        traci.simulationStep()
#        print("State0: {}".format(state[0]))
#        print(step)
        vehs = traci.vehicle.getIDList()
#        print(vehs)
        pos = {}
#        for v in vehs:
#        for name in ["taxi1"]:#, "taxi2", "taxi3"]:
        if (carName != ""):
            vehEdgeID_new = traci.vehicle.getRoadID(carName)
            if( vehEdgeID_new == appEdgeID[0] and ((step - step_) > 400) ):
                print("Waiting for the customer")
                print(stopCount)
                print(traci.vehicle.getSpeed(carName))
                if (int(traci.vehicle.getSpeed(carName)) == 0 and (stopCount > 150) ):
                    step_ = step
                    vehEdgeID = traci.vehicle.getRoadID(carName)
                    route2 = traci.simulation.findRoute(vehEdgeID,destEdgeID[0]).edges
                    print("Towards the final stop")
                    traci.vehicle.setRoute(carName, route2)
                    print(route2)
                    print(destEdgeID[0])
                    global isAppInCar
                    isAppInCar = 1
                    traci.vehicle.resume(carName)
                    traci.vehicle.setStop(carName, destEdgeID[0], flags=traci.constants.STOP_PARKING)
                stopCount+=1
            pos2D = traci.vehicle.getPosition(carName)
            pos[carName] = traci.simulation.convertGeo(pos2D[0], pos2D[1])
            #convertRoad(self, x, y, isGeo=False)
            topic = "pos/slovenia/ljubljana"
            payload = json.dumps({"id":carName, "lon":pos[carName][0], "lat":pos[carName][1], "isAppInCar":isAppInCar})
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

        step += 1
    mqttClient.disconnect()
    mqttClient.loop_stop()
    traci.close()
    sys.stdout.flush()

# states that comes from mqttOnMessage
def stateAction(state):
    ######################   REQUEST FOR ALL (DURATION)   ###################
    if(state[0] == "request"):
        global appEdgeID
        global destEdgeID
        global carName
        global route2
        appEdgeID = traci.simulation.convertRoad(dataJson["appLon"], dataJson["appLat"], True)
        destEdgeID = traci.simulation.convertRoad(dataJson["destLon"], dataJson["destLat"], True)
        route2 = traci.simulation.findRoute(appEdgeID[0],destEdgeID[0]).edges
        route2time = 0
        for edge in route2 :
            mtime2 = traci.edge.getTraveltime(edge)
            if (mtime2 > 20.0):
                print("STRANGE EST. TIME FOR NODE: {}!!!!!!!!!!!!!!!!!!!!!!!!!!".format(edge))
                print(mtime2)
                mtime2 = 0.0
            route2time += mtime2

        for car in ["taxi1", "taxi2", "taxi3"]:
            print("For the vehicle :{}".format(car))
            vehEdgeID = traci.vehicle.getRoadID(car)
#            print("VehEdgeID :", vehEdgeID)
            route1 = traci.simulation.findRoute(vehEdgeID,appEdgeID[0]).edges
#            print("Route1 :", route1)
            route1time = 0
            for edge in route1 :
                mtime = traci.edge.getTraveltime(edge)
                if (mtime > 20.0):
                    print("STRANGE EST. TIME FOR NODE: {}!!!!!!!!!!!!!!!!!!!!!!!!!!".format(edge))
                    print(mtime)
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
        carName = state[1]
        appEdgeID = traci.simulation.convertRoad(dataJson["appLon"], dataJson["appLat"], True)
        print("appEdgeID :", appEdgeID)
        destEdgeID = traci.simulation.convertRoad(dataJson["destLon"], dataJson["destLat"], True)
        print("destEdgeID :", destEdgeID)
        route2 = traci.simulation.findRoute(appEdgeID[0],destEdgeID[0]).edges

        print("For the vehicle :{}".format(carName))
        vehEdgeID = traci.vehicle.getRoadID(carName)
        print("vehEdgeID :", vehEdgeID)
        route1 = traci.simulation.findRoute(vehEdgeID,appEdgeID[0]).edges
        print("route1 :", route1)

        #getDistanceRoad(self, edgeID1, pos1, edgeID2, pos2, isDriving=False)
        distance1 = traci.simulation.getDistanceRoad(vehEdgeID, 0, appEdgeID[0], 0, isDriving=True)
        distance2 = traci.simulation.getDistanceRoad(appEdgeID[0], 0, destEdgeID[0], 0, isDriving=True)
        print(distance1)
        print(distance2)
        distance = int(distance1 + distance2)

        ###############   ETHEREUM CONTRACT - SET DISTANCE   ###########
        with open("./web/mqttMaps/src/ethereum/build/MobilityAccountABI.json") as f:
            info_json = json.load(f)
        abi = info_json

        w3 = Web3(HTTPProvider(RINKEBY))
        profile = w3.eth.contract(address=getProfileADDR(carName), abi=abi)
        pw = getpass(prompt='Enter the password for decryption: ')

        with open('./web/mqttMaps/src/ethereum/{}.json'.format(carName)) as keyfile:
            encrypted_key = keyfile.read()
        pk = w3.eth.account.decrypt(encrypted_key, pw)

        transaction = {
#            'value': Web3.toWei(0.001, "ether"),
            'gas': 500000,
            'gasPrice': w3.eth.gasPrice,
            'nonce': w3.eth.getTransactionCount(getVehicleADDR(carName))
        }
        try:
            txn = profile.functions.setDistance(distance).buildTransaction(transaction)
            signed_txn = w3.eth.account.signTransaction(txn, private_key=pk)
            w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        except Exception as e:
            print(e)
        ################################################################
        rideID = random.randint(1, 999999999999)
        print("Pay ride id:{}, with amount: {:.5f} ether to contract: {}".format(rideID, distance / METER_PER_ETHER, getProfileADDR(carName)))

        topic = "req_veh/" + dataJson["id"] + "/pay"
        payload = json.dumps({"rideID":rideID, "amount":"{}".format(distance/METER_PER_ETHER), "address":getProfileADDR(carName) })
        mqttClient.publish(topic,payload)

        # Stay in while loop and check on interval if generated ride is paied
        # TODO: move this funcionality into separate thread and use events!!
        isPaid = profile.functions.getIsPaid(rideID).call()
        intervalCount = 0
        while ( not isPaid ):
            isPaid = profile.functions.getIsPaid(rideID).call()
            time.sleep(5)
        print("Thank you for your payment!")
        print("Taxi is on the way!")

        if traci.vehicle.getSpeed(carName) == 0:
            traci.vehicle.setRoute(carName, route1)
            global isAppInCar
            isAppInCar = 0
            traci.vehicle.resume(carName)
            traci.vehicle.setStop(carName, appEdgeID[0], flags=traci.constants.STOP_PARKING)

def getVehicleADDR(_carName):
    if _carName == "taxi1":
        return '0xB76AC1f39edCa9087dBcaa832B3169cCE0E8Dc65'
    elif _carName == "taxi2":
        return '0xEFB3164881f0B9E3b8b498951A9047fD24dACE4c'
    elif _carName == "taxi3":
        return '0x28185AF737F17459CE7176905351a09b53943104'

def getProfileADDR(_carName):
    if _carName == "taxi1":
        return '0x37D2bF2Fe9f225336784337Ed581A2FDd7bd4952'
    elif _carName == "taxi2":
        return '0xf1080ce12d54d5d8076D3FA5A8aA48FaA2Ef0e17'
    elif _carName == "taxi3":
        return '0x06D2e345DBd7899254CF2d6082B415FE2E0ceE68'

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

#    print("---------------------------------")
#    print("MQTT message:")
    print("Topic: " + msg.topic)
#    print("payload: " + msg.payload)
#    if traci.vehicle.getSpeed("right_0") == 0:
#        traci.vehicle.resume("right_0")
#    traci.vehicle.setRoute("right_0", ["10", "03", "30"])
#    traci.vehicle.setStop("right_0", "30", 400.0, flags=traci.constants.STOP_PARKING)


def main():
    global mqttClient
    mqttClient = mqtt.Client("mobiClient_"+str(random.randint(1, 1000)))
    mqttClient.on_connect = mqttOnConnect
    mqttClient.on_message = mqttOnMessage
    mqttClient.username_pw_set("mobi", mqttPasswd);

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

    # get password for the mqtt user
    mqttPasswd = getpass(prompt='Enter the password for mqtt mobi user: ')

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
