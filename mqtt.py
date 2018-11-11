import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("data/#")
    print("Subscribed")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
#    if msg.topic == "sigfox/survey":
#    if msg.payload == "EXIT":
    print("Topic: " + msg.topic)
    print("payload: " + msg.payload)


def main():
    client = mqtt.Client("mobiClient")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost")

    # Loop forever
    try:
        client.loop_forever()
    # Catches SigINT
    except KeyboardInterrupt:
        client.disconnect()
        print("Exiting main thread")
        time.sleep(2.0)

if __name__ == '__main__':
    main()
