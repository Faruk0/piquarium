import os
from w1thermsensor import *
import RPi.GPIO as GPIO
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_led_ok = 17
temp_led_ko = 18
ph_led_ok = 22
ph_led_ko = 23

tempmin = 24
tempmax = 26
phmin = 8
phmax = 8.4


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(temp_led_ok, GPIO.OUT)
    GPIO.setup(temp_led_ko, GPIO.OUT)
    GPIO.setup(ph_led_ok, GPIO.OUT)
    GPIO.setup(ph_led_ko, GPIO.OUT)
    while True:
        temperatures = []
        for sensor in W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18B20]):
            temperatures.append(sensor.get_temperature())

        if temperatures[0] > tempmax:
            GPIO.output(temp_led_ko, True)
            GPIO.output(temp_led_ok, False)
            print("trop chaud")
        elif temperatures[0] < tempmin:
            GPIO.output(temp_led_ko, True)
            GPIO.output(temp_led_ok, False)
            print("trop froid")
        else:
            GPIO.output(temp_led_ko, False)
            GPIO.output(temp_led_ok, True)
            print("ok")
