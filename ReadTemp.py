import os
import sys

def sensor_def():
    sensor_list = []
    for sensor_id in os.listdir('/sys/bus/w1/devices'):
        if sensor_id != 'w1_bus_master1':
            sensor_list.append(sensor_id)
    return sensor_list

def read_from_sensor(sensor):
    list_of_temps_in_celcius =[]
    try:
        for item in range(len(sensor)):
            location = '/sys/bus/w1/devices/' + sensor[item] + '/w1_slave'
            file = open(location)
            text = file.read()
            file.close()
            sensor_data = text.split("\n")[1]
            temperature_data = sensor_data.split(" ")[-1]
            list_of_temps_in_celcius.append(round(float(temperature_data[2:])/1000,1))
    except:
        return list_of_temps_in_celcius

    return list_of_temps_in_celcius

def kill():
    quit()

if __name__ == '__main__':
    Serial_Num = []
    try:
        Serial_Num = sensor_def()
        print read_from_sensor(Serial_Num)
    except KeyboardInterrupt:
        print "Exiting..."
        sys.exit(0)
