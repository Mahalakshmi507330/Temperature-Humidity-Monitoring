import dht
import time
import network
import urequests
from machine import Pin
sensor = dht.DHT22(Pin(15))
led = Pin(2, Pin.OUT)
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST", "")
print("Connecting to Wi-Fi...")
while not wifi.isconnected():
    time.sleep(1)
print("Wi-Fi connected!")
print(wifi.ifconfig())
API_KEY = "TD210S9JCKQC978B"
while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print("-------------------------")
        print("Temperature:", temperature, "C")
        print("Humidity:", humidity, "%")
        if temperature >= 30:
            led.on()
            print("LED: ON - High Temperature")
        else:
            led.off()
            print("LED: OFF - Normal Temperature")
        url = (
            "https://api.thingspeak.com/update"
            "?api_key={}"
            "&field1={}"
            "&field2={}"
        ).format(API_KEY, temperature, humidity)
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Error:", e)
    time.sleep(15)
