import ReadTemp
import SerialNumberReading
import sys
import Read_Scale
import gps_position_json
import Pi_Camera
import json

def get_measurements():
    # Get the image in binary format
    binary_img = Pi_Camera.take_picture()
	
    # Get devices Serial number
    device_id = SerialNumberReading.getserial()

    # Get the reading from the scale
    v_weight = round(Read_Scale.get_measurement(2)/1000,2)

    # Get location
    v_gps_location = gps_position_json.get_location()

    # Get inner,outer temperature
    sensor_cd = ReadTemp.sensor_def()
    sensor_mp = ReadTemp.read_from_sensor(sensor_cd)
    v_inner_temperature = sensor_mp[0]
    v_outer_temperature = sensor_mp[1]
    if len(sensor_mp) == 0:
        v_inner_temperature = -99
        v_outer_temperature = -99

    data_to_transmit = {}
    data_to_transmit["serial_number"] = device_id.replace("'", "")
    data_to_transmit["image_binary"] = binary_img
    data_to_transmit["inner_temperature"] = v_inner_temperature
    data_to_transmit["outer_temperature"] = v_outer_temperature
    data_to_transmit["gps_latitude"] = v_gps_location[0]
    data_to_transmit["gps_longitude"] = v_gps_location[1]
    data_to_transmit["weight"] = v_weight
	
    # Prepare the string of data to be sent
    json_data = json.dumps(data_to_transmit,indent=1)

    return json_data
	
if __name__ == "__main__":
    print get_measurements()
