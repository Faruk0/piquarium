import os
from time import sleep
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import src.i2c_demo as i2c

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

calibration = ""
aquariophile = "abraham.sylla@epita.net"

tempg = 4
tempr = 27
tempb = 17

phg = 13
phr = 26
phb = 19

tempmin = 24
tempmax = 26
phmin = 8
phmax = 8.4


def send_alert(sonde, niveau):
    receiver_email = aquariophile  
    sender_email = "w.world2345@laposte.net" 
    password = 'Annecy2019!'

    msg = MIMEMultipart()
    msg["Subject"]= "I am a fish and I need air"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    message = "le niveau de " + sonde + " est à " + niveau
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.laposte.net', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(sender_email, password)
    try:
       di = mailserver.sendmail(sender_email, msg.as_string())
       print(di)
    except:
       print('mail not sent')
    mailserver.quit()



def settempled(value):
    if value > tempmax:
        GPIO.output(tempr, 1)
        GPIO.output(tempg, 0)
        send_alert("température", value)
    elif value < tempmin:
        GPIO.output(tempr, 1)
        GPIO.output(tempg, 0)
        send_alert("température", value)
    else:
        GPIO.output(tempr, 0)
        GPIO.output(tempg, 1)

def setphled(value):
    if value > phmax:
        GPIO.output(phr, 1)
        GPIO.output(phg, 0)
        send_alert("ph", value)
    elif value < phmin:
        GPIO.output(phr, 1)
        GPIO.output(phg, 0)
        send_alert("ph", value)
    else:
        GPIO.output(phr, 0)
        GPIO.output(phg, 1)





if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(tempg, GPIO.OUT)
    GPIO.setup(tempr, GPIO.OUT)
    GPIO.setup(tempb, GPIO.OUT)
    GPIO.setup(phg, GPIO.OUT)
    GPIO.setup(phr, GPIO.OUT)
    GPIO.setup(phb, GPIO.OUT)
    GPIO.output(tempr, 1)
    GPIO.output(tempg, 0)
    GPIO.output(tempb, 0)
    GPIO.output(phr, 1)
    GPIO.output(phg, 0)
    GPIO.output(phb, 0)
    i2cdevice_list = i2c.get_devices()
    i2cdevice = i2cdevice_list[0]
    i2cdevice.query("Import," + calibration)

    while True:
        temperatures = []
        for sensor in W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18B20]):
            temperatures.append(sensor.get_temperature())

        settempled(temperatures[0])

        ph = float(i2cdevice.query("r"))

        setphled(ph)

        sleep(60)
