import RPi.GPIO as GPIO
import time
import sys
from hx711_C import HX711

def cleanAndExit():
    #print "Cleaning & Exiting..."
    GPIO.cleanup()
    sys.exit()

def get_measurement(number_of_samples):
    hx = HX711(5, 6)
    hx.set_reading_format("LSB", "MSB")
	# The value of the reference that is used depends on the construction.
	# Different construction will lead to different calibration
    hx.set_reference_unit(442)
    hx.reset()
    #hx.tare()
    weight = []
    for i in range(number_of_samples):
        try:
            weight.append(max(0, int(hx.get_weight(3))))
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
    return float(max(0,(sum(weight) / len(weight))-18990))

if __name__ == '__main__':
    print round(get_measurement(2)/1000,2)
    cleanAndExit()
