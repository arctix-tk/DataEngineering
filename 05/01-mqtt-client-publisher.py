# download mosquitto broker https://mosquitto.org/download/
# start mosquitto broker with default configuration
# https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
# package paho-mqtt
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import numpy as np
import math
import random
# This is the Publisher


# def create_values(start):
#     l = np.array([(random.uniform(-20,20)+20479)*math.sin((775*2*math.pi)*(z := x/1024 if x else x))
#                  for x in range(start, start+1024)], dtype=np.int16)
#     return l

def create_values_time(start):
    l = []
    t = []
    for x in range(start, start+1024):
        l.append((random.uniform(-20,20)+20479)*math.sin((775*2*math.pi)*(z := x/1024 if x else x)))
        t.append(datetime.now())
    
    return np.array(l,dtype=np.int16), t

# def create_values(start):
    

client = mqtt.Client()
client.connect("localhost", 1883, 60)
i = 0


while i < 600:
    # values und creation time
    v,mt  = create_values_time(i*1024)
    # als string casten damit man encode kann
    t = str(datetime.now())
    
    # erstellen bytearray und hinzufügen des zeitstempel und der werte
    b = bytearray()
    b.extend(t.encode('utf-8'))
    b.extend(v.tobytes())
  
    # # erste aufgabe
    client.publish("sens1/binary", b)
    
    for n in range(0,len(v)):
       client.publish("sens1/test",f"{t},{v[n]},{mt[n]},{i}")
    time.sleep(1)  # sleep for 10 seconds before next call
    i += 1
client.disconnect()
