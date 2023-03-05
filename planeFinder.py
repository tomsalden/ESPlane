import time
import _thread
import gc
import urequests
import ujson

import settings
import classes
import networkManager

memoryCounter = 0
memoryErrorSignal = False

Latitude = 0
Longitude = 0

previousUpdateTime = 0

def updatePlanes():
    divideArea()

    while settings.main_updateTime + settings.main_timeout > time.time():       #Check if main did not timeout, otherwise stop the loop
        updateThreadTime()                                                      #Update the time this thread last ran
        gc.collect()
        print("Thread ID: ", _thread.get_ident())
        print("Memory left: ", gc.mem_free())
        settings.led.value(not settings.led.value())
        tempPlanes = planeTracking(settings.myLat,settings.myLon,settings.importantAirplanes)
        while memoryErrorSignal:
            print("Trying again! Thread: ", _thread.get_ident())
            settings.thread_Plane_updateTime = time.time()
            tempPlanes = planeTracking(settings.myLat,settings.myLon,settings.importantAirplanes)

        settings.planesReady = False
        settings.planes = tempPlanes
        settings.planesReady = True
        print(settings.planes.name)
    print("Planefinder has been shut down")

def updateThreadTime():
    #Update the time the thread ran previously. If this is different than what was saved before, another thread probably is running. In that case, close this thread
    #Check previous time, if it is different that before, send stopsignal
    if previousUpdateTime != settings.thread_Plane_updateTime:
        settings.thread_Plane_stopsignal = True

    #Update the updatetime and save it to compare for the next time
    previousUpdateTime = time.time()
    settings.thread_Plane_updateTime = previousUpdateTime

def divideArea():
    global Latitude
    global Longitude

    Latitude = [settings.areaMinLat, settings.areaMaxLat]
    Longitude = [settings.areaMinLon, settings.areaMaxLon]

    latChunk = settings.areaMaxLat - settings.areaMinLat
    lonChunk = settings.areaMaxLon - settings.areaMinLon

    latDividedChunk = latChunk / settings.areaDivisions
    lonDividedChunk = lonChunk / settings.areaDivisions

    for i in range(settings.areaDivisions-1):
        Latitude.insert(i+1,Latitude[i] + latDividedChunk)
        Longitude.insert(i+1,Longitude[i] + lonDividedChunk)

def planeTracking(myLat,myLon,importantAirplanes):
    global memoryErrorSignal
    global memoryCounter

    global Latitude
    global Longitude

    selectedPlaneName = []
    selectedPlaneLat = []
    selectedPlaneLon = []
    selectedPlaneDistance = []
    selectedPlaneAltitude = []
    selectedPlaneType = []
    selectedPlaneRegistration = []
    selectedPlaneHeading = []
    selectedPlaneSpeed = []
    selectedPlaneTimestamp = []

    memoryErrorSignal = False
    


    for i in range(settings.areaDivisions):
        for j in range(settings.areaDivisions):
            updateThreadTime()

            #Check if there is a stopsignal
            if settings.thread_Plane_stopsignal:
                print("Stopping plane manager")
                settings.thread_Plane_stopped = True
                _thread.exit()

            #Check if main timed out
            if settings.main_updateTime + settings.main_timeout < time.time():
                print("Stopping plane manager")
                settings.thread_Plane_stopped = True
                _thread.exit()
                
            response = []
            Bounds = str(Latitude[i+1]) + "," + str(Latitude[i]) + "," + str(Longitude[j]) + "," + str(Longitude[j+1])
            URL =  "http://data-live.flightradar24.com/zones/fcgi/feed.js?bounds=" + Bounds + "&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&vehicles=0&estimated=1&maxage=14400&gliders=0&stats=0"  
            headers = {'Content-Type': 'application/json', 'Connection': 'Close'}
            try:
                response = urequests.get(url = URL, headers = headers)
                #response = urequests.head(URL)
                #print(response.text)
            except OSError as e:
                print("Error detected: ", e)
                if e.errno == -202 or e.errno == 113 or e.errno == 104:
                    print("Error 202, resetting connection")
                    networkManager.connectNetwork()
                if e.errno != errno.ECONNRESET:
                    raise # Not error we are looking for
                pass # Handle error here.

            # if response.text == []:
            #     continue
            #Parse the response and format it in json format
            try:
                parsed = ujson.loads(response.text)
            except AttributeError:
                print("Attribute Error")
                response.close()
                continue
            except OSError:
                print("OS Error")
                response.close()
                continue
            except MemoryError:
                print("Memor error!!!")
                memoryErrorSignal = True
                continue

            response.close()
            print("Response from area: " + str(i) + ", " + str(j))

            for attribute, value in parsed.items():
                if attribute != 'version' and attribute != 'full_count':
                    if any(x in str(value[16]) for x in importantAirplanes):
                        selectedPlaneName.append(str(value[16]))
                        selectedPlaneLat.append(value[1])
                        selectedPlaneLon.append(value[2])
                        selectedPlaneDistance.append(((abs(value[1]-myLat))**2+(abs(value[2]-myLon))**2)**0.5)
                        selectedPlaneAltitude.append(value[4])
                        selectedPlaneType.append(str(value[8]))
                        selectedPlaneRegistration.append(str(value[9]))
                        selectedPlaneHeading.append(value[3])
                        selectedPlaneSpeed.append(value[5])
                        selectedPlaneTimestamp.append(value[10])

    if memoryErrorSignal:
        if settings.areaDivisions < settings.maxAreaDivisions:
            settings.areaDivisions = settings.areaDivisions + 1
            divideArea()
            memoryCounter = 0

    #Reset the area division to see if it is less busy
    if memoryCounter > 20:
        memoryCounter = 1
        settings.areaDivisions = settings.areaDivisions - 1
        divideArea()

    if settings.areaDivisions > 1:
        memoryCounter = memoryCounter +1

    planes = classes.selectedPlanes(selectedPlaneName,selectedPlaneLat,selectedPlaneLon,selectedPlaneDistance,selectedPlaneAltitude,selectedPlaneSpeed,selectedPlaneHeading,selectedPlaneType,selectedPlaneRegistration,selectedPlaneTimestamp)
    return planes
