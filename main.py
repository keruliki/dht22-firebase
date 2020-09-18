import pyrebase

import RPi_I2C_driver
from time import *

config = {
    "apiKey": "AIzaSyA8S1-UF-7Jf8jUt-Ja6Gby7FoiuJnpErI",
    "authDomain": "refeercontainer-12d2e.firebaseapp.com",
    "databaseURL": "https://refeercontainer-12d2e.firebaseio.com",
    "projectId": "refeercontainer-12d2e",
    "storageBucket": "refeercontainer-12d2e.appspot.com",
    "messagingSenderId": "453272591416",
    "appId": "1:453272591416:web:fa5824049e2a6f3d851acd"
}

mylcd = RPi_I2C_driver.lcd()

mylcd.lcd_display_string("RPi I2C test", 1)
mylcd.lcd_display_string(" Custom chars", 2)

sleep(2) # 2 sec delay

mylcd.lcd_clear()
firebase = pyrebase.initialize_app(config)
db = firebase.database()
# data to save


db.set(data)


import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")
        
        
    
    
    data = {
        "humidity": "20",
        "temperature" : "10",
        "object": "1"
    }
    db.update(data)
    
    time.sleep(1)
    

