import serial
import time
import os
import string
import pynmea2
import sys
import requests
import json
from datetime import datetime,timedelta

def get_location():
    location =[]
    lat=0.0
    lng=0.0
    started = datetime.now()
    now_plus_2 = started + timedelta(minutes = 2)

    # Try to get GPS data within 2 minutes
    while now_plus_2 > datetime.now() and lat == 0.0:
        try:
            ser = serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=0.5)
            data = pynmea2.NMEAStreamReader()
            newdata = ser.readline()
            if newdata[0:6] == '$GPRMC':
                # parse the data
                newmsg = pynmea2.parse(newdata)
                lat = newmsg.latitude
                lng = newmsg.longitude
                time.sleep(0.7)
        except:
            sys.exit()
    ser.close()
    location.extend((lat,lng))
    return location

if __name__ == "__main__":
    gps_location = get_location()
    print ("Latitude:" + str(gps_location[0]) + ',' + "Longitude:" + str(gps_location[1]))
