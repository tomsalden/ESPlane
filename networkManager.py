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
    print("Network connected")
    settings.networkConnection = True

def connectToNetwork():
    station.disconnect()
    while not station.isconnected():
        for ssid, psk in WifiCredentials.networkDetails:
            try:
                station.connect(ssid,psk)
            except OSError as e:
                time.sleep(0.5)
                
            #Wait for the connection to succeed or fail
            for _ in range(20):
                if station.isconnected():
                    print("Connected to: ", ssid)
                    settings.networkConnection = True
                    break
                else:
                    time.sleep(0.5)

            if station.isconnected():
                break

def checkConnection():
    return station.isconnected()