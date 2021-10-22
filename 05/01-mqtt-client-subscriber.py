# download mosquitto broker https://mosquitto.org/download/
# start mosquitto broker with default configuration
# https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
# package paho-mqtt
import paho.mqtt.client as mqtt
import json
import pyodbc
from datetime import datetime
import numpy as np
# This is the Subscriber


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sens1/binary")
    client.subscribe("sens1/test")


def on_message(client, userdata, msg):
    m = msg.payload
    # ersten 26 byte sind der Zeitstempel
    t = m[:26]
    # string decodieren und umwandeln in datetime object
    created_at = datetime.fromisoformat(t.decode())
    received_at = datetime.now()
    data = m[26:]
    # insert in tabelle
    cursor.execute("insert into TableBinary (created_at,received_at,sensor_data) values (?,?,?)",(created_at,received_at,data))
    cnxn.commit()

    # prüfen ob array richtig angekommen ist
    #  l = np.frombuffer(m[26:],dtype=np.int16)
    #  print(type(l))
    #  print(l)


def on_message_datapackage(client, userdata, msg):
    received_at = datetime.now()
    m = msg.payload.decode().split(',')
    created_at = datetime.fromisoformat(m[2])
    started_at = datetime.fromisoformat(m[0])
    package_id = int(m[3])
    value = int(m[1])
    cursor.execute("insert into TableDataPackage (package_id,started_at,created_at,received_at,sensor_data) values (?,?,?,?,?)",(package_id,started_at,created_at,received_at,value))
    cnxn.commit()

# hier eigene Werte für Server und UID eingeben UID -> Benutzername 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+"TOBIAS-PC" +
                      ';DATABASE='+"MQTT"+';UID='+"TOBIAS-PC\TK"+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

client = mqtt.Client()
client.connect("localhost", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("sens1/test", on_message_datapackage)

client.loop_forever()
