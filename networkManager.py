import time
import network
import settings
import WifiCredentials

def initialiseNetwork():
    global station
    station = network.WLAN(network.STA_IF)
    station.active(True)

def connectNetwork():
    station.disconnect()
    while not station.isconnected():
        settings.led.value(not settings.led.value())
        print("Connecting...")
        try:
            station.connect(WifiCredentials.wifi_ssid, WifiCredentials.wifi_password)
        except OSError as e:
            time.sleep(1)

        if station.isconnected():
            continue

        try:
            station.connect(WifiCredentials.wifi_ssid2, WifiCredentials.wifi_password2)
        except OSError as e:
            time.sleep(1)

def checkConnection():
    return station.isconnected()