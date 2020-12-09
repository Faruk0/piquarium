import os
from w1thermsensor import *
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

if __name__ == '__main__':
    while True:
        temperatures = []
        for sensor in W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18B20]):
            temperatures.append(sensor.get_temperature())
        print("test")
