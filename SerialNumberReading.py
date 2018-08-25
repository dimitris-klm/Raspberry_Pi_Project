import os
from datetime import datetime
import requests
import json
import random

def getserial():
  # Extract serial from cpuinfo file
  cpu_serial = "-000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpu_serial = "'" + line[10:26] + "'"
    f.close()
  except:
    cpu_serial = "ERROR000000000"
  return cpu_serial

if __name__ == '__main__':
    print getserial()
