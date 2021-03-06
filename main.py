from pyrebase import pyrebase

import RPi_I2C_driver
from time import *

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "m",
    "messagingSenderId": "",
    "appId": ""
}

mylcd = RPi_I2C_driver.lcd()

mylcd.lcd_display_string("Refeer Conteiner", 1)
mylcd.lcd_display_string("System", 2)

sleep(2) # 2 sec delay

mylcd.lcd_clear()
firebase = pyrebase.initialize_app(config)
db = firebase.database()
# data to save

data = {
        "humidity": "0",
        "temperature" : "0",
        "object": "1"
}
    
db.set(data)


import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

buzzer = 18
led = 24

GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)

#set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

object_p = 0

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time()
    StopTime = time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
def warningh():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Warning!", 1)
    mylcd.lcd_display_string("Humidity Exceed", 2)
    GPIO.output(led, True)	
    sleep(1)
    

def warning():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Warning!", 1)
    mylcd.lcd_display_string("Temperature Exceed", 2)
    GPIO.output(led, True)	
    sleep(1)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")
    
    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)
    sleep(1)
    
    if dist < 100:
        object_p = 1
    
    else:
        object_p = 0
        
    if temperature > 5:
        warning()
    
    if humidity > 85:
        warningh()
    
    
        
    
    data = {
        "humidity": humidity,
        "temperature" : temperature,
        "object": object_p
	}
    
    db.update(data)
    
    display_t = "Temp:{0:0.1f}*C".format(temperature)
    display_h = "Humid:{0:0.1f}% ".format(humidity)
    mylcd.lcd_clear()
    mylcd.lcd_display_string(display_t, 1)
    mylcd.lcd_display_string(display_h, 2)
    sleep(1)
    
		
    sleep(1)
