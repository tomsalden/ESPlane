import _thread
import time
import ntptime
import gc

import settings
import servoControl
import OLEDControl
import networkManager
import planeFinder
import locationManager

#############   Variables             #############


#############   Initialise components #############

gc.enable

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

#############   Main loop          #############
#Continually check if a connection is active, check if all threads are running and restart them if necessary
while True:
    settings.main_updateTime = time.time()
    time.sleep(1)                                                       #Sleep for some time to limit update frequency

    if not networkManager.checkConnection():                            #Test for network connection, restart connection if not
        print("Network is down, reconnecting!!")
        networkManager.connectNetwork()

    #Check if the planefinder thread is still working, otherwise restart
    if settings.thread_Plane_updateTime + settings.thread_Plane_timeout < time.time():
        print("Send stop signal to plane manager")
        settings.thread_Plane_stopsignal = True
        
        if settings.thread_Plane_stopped:
            gc.collect()
            print("Start plane manager")
            settings.thread_Plane_stopsignal = False
            settings.thread_Plane_updateTime = time.time()
            _thread.start_new_thread(planeFinder.updatePlanes,())
    
    if not settings.planesReady:
        continue

    #Check if the planefinder thread is still working, otherwise restart
    if settings.thread_location_updateTime + settings.thread_location_timeout < time.time():
        print("Start location manager")
        settings.thread_location_updateTime = time.time()
        _thread.start_new_thread(locationManager.updateLocation,())


    #Check if the servo thread is still working, otherwise restart
    if settings.thread_Servo_updateTime + settings.thread_Servo_timeout < time.time():
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
