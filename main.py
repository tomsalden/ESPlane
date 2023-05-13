import machine
import _thread
import time
import ntptime
import gc

from buzzer_music import music

import settings
import servoControl
import OLEDControl
import networkManager
import planeFinder
import locationManager

#############   Variables             #############


#############   Initialise components #############

gc.enable

#https://onlinesequencer.net/

startupSong = music(settings.startupSound, pins=[machine.Pin(4)], looping=False)

while startupSong.stopped == False:
    startupSong.tick()
    time.sleep(0.04)


# buzzerPin = machine.Pin(4, machine.Pin.OUT)
# buzzerPWM = machine.PWM(buzzerPin)

# buzzerPWM.duty(112)
# buzzerPWM.freq(1000)

# time.sleep_ms(100)

# buzzerPWM.freq(1500)

# time.sleep_ms(100)

# buzzerPWM.freq(1)
# buzzerPWM.deinit()
# buzzerPin.value(1)

# Setup servo's and OLED
print("Initialising servos")
servoControl.initServos()
print("Initialising OLED")
OLEDControl.initOLED()

#Connect to network
print("Connecting to network")
networkManager.initialiseNetwork()
networkManager.connectToNetwork()
OLEDControl.networkConnected()

#Update callsign and models
print("Updating airplane list")
planeFinder.updateAirplaneList()

#Set correct time
correctTime = False
while not correctTime:
    try:
        ntptime.settime()
    except OSError:
        print("Retrying to get time")
        continue
    correctTime = True
print("Current time (seconds since epoch): ")
print(time.time())
startTime = time.time()

#############   Main loop          #############
#Continually check if a connection is active, check if all threads are running and restart them if necessary
while True:
    try:
        settings.main_updateTime = time.time()
        time.sleep(1)                                                       #Sleep for some time to limit update frequency

        if not networkManager.checkConnection():                            #Test for network connection, restart connection if not
            print("Network is down, reconnecting!!")
            networkManager.connectToNetwork()

        if not settings.networkConnection:                            #Test for network connection, restart connection if not
            print("Network is stated down, reconnecting!!")
            networkManager.connectToNetwork()

        #Check if the planefinder thread is still working, otherwise restart
        if settings.thread_Plane_updateTime + settings.thread_Plane_timeout < time.time():
            print("Send stop signal to plane manager")
            settings.thread_Plane_stopsignal = True
            # Soms start PlaneManager op het vereerde moment, dat de signalen verkeerd om zijn

            if settings.thread_Plane_stopped:
                gc.collect()
                print("Start plane manager")
                settings.thread_Plane_stopsignal = False
                settings.thread_Plane_updateTime = time.time()
                _thread.start_new_thread(planeFinder.updatePlanes,())

        #If there are no planes in 5 seconds, show that there are no planes
        if not settings.planesReady:
            if settings.main_updateTime > startTime + 10:
                OLEDControl.noPlanesOLED()
            continue

        #Check if the planefinder thread is still working, otherwise restart
        if settings.thread_location_updateTime + settings.thread_location_timeout < time.time():
            print("Start location manager")
            settings.thread_location_updateTime = time.time()
            _thread.start_new_thread(locationManager.updateLocation,())


        #Check if the servo thread is still working, otherwise restart
        if settings.thread_Servo_updateTime + settings.thread_Servo_timeout < time.time() and settings.servoEnabled == True:
            print("Start servo manager")
            settings.thread_Servo_updateTime = time.time()
            _thread.start_new_thread(servoControl.updateServos,())

        #Restart main loop if no OLED screen is connected
        if not settings.oledConnected:
            continue

        #Check if the servo thread is still working, otherwise restart
        if settings.thread_OLED_updateTime + settings.thread_OLED_timeout < time.time():
            print("Start OLED manager")
            settings.thread_OLED_updateTime = time.time()
            _thread.start_new_thread(OLEDControl.updateOLED,())
    except:
        machine.reset()
