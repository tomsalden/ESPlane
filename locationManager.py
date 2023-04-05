import time
import math

import settings
import classes

def updateLocation():
    printLimiter = 0
    while settings.main_updateTime + settings.main_timeout > time.time():
        settings.thread_location_updateTime = time.time()
        time.sleep(1)
        #Check if plane information can be accessed
        if not settings.planesReady:
            continue
        if not settings.planes:
            continue
        #Check if there are any planes at all
        if not settings.planes.name:
            # print("No airplanes available, no coordinates")
            continue

        #Find the highest plane
        planesAltitude = []
        for i in range(len(settings.planes.name)):
            planesAltitude.append(getAltitude(settings.planes.lat[i],settings.planes.lon[i],settings.planes.altitude[i],settings.myLat,settings.myLon,settings.myAlt))
        highestPlane = max(planesAltitude)
        indexHighest = planesAltitude.index(highestPlane)

        #Select the plane to get the details from
        selectedIndex = (indexHighest + settings.selectedPlane) % len(settings.planes.name)
        selectedPlane = classes.selectedPlanes(settings.planes.name[selectedIndex],settings.planes.lat[selectedIndex],settings.planes.lon[selectedIndex],settings.planes.distance[selectedIndex],settings.planes.altitude[selectedIndex],settings.planes.speed[selectedIndex],settings.planes.heading[selectedIndex],settings.planes.type[selectedIndex],settings.planes.registration[selectedIndex],settings.planes.timestamp[selectedIndex])
        settings.currentPlane = selectedPlane

        #find out how new the data is, interpolate the distance travelled and get up-to-date coordinates
        timeTravelled = time.time() - (selectedPlane.timestamp - 946684800) #Compensate for partial epoch
        planeSpeed_meter_second = selectedPlane.speed / 1.944
        distanceTravelled = planeSpeed_meter_second * timeTravelled
        [newLat, newLon] = getNewCoords(selectedPlane.lat, selectedPlane.lon, distanceTravelled, selectedPlane.heading)

        #Calculate the direction from my location and the altitude angle
        newAltAngle = getAltitude(newLat, newLon, selectedPlane.altitude, settings.myLat, settings.myLon, settings.myAlt)
        newDirection = getDirection(newLat, newLon, settings.myLat, settings.myLon)
        newDistance = getDistance(newLat, newLon, settings.myLat, settings.myLon)

        #Lock the geomatics, update the value and unlock
        settings.geomaticsReady = False
        settings.geomatics = classes.updatedGeomatis(newDistance,newAltAngle,newDirection)
        settings.geomaticsReady = True

        printLimiter = printLimiter + 1
        if printLimiter > 10:
            print("Selected plane:", selectedPlane.name, "Distance:", newDistance/1000)
            printLimiter = 0
    
    print("Location manager has been shut down")



def getAltitude(newLat,newLon,newAlt,curLat, curLon, curAlt):
    lat1 = math.radians(curLat)
    lon1 = math.radians(curLon)
    lat2 = math.radians(newLat)
    lon2 = math.radians(newLon)

    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = 6371*1000*c

    altangle = math.atan((newAlt*0.3048-curAlt)/d)
    altangle = math.degrees(altangle)
    return altangle

def getDirection(newLat,newLon,curLat, curLon):
    lat1 = math.radians(curLat)
    lon1 = math.radians(curLon)
    lat2 = math.radians(newLat)
    lon2 = math.radians(newLon)

    x = math.cos(lat2) * math.sin(lon2-lon1)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1)

    direction = math.degrees(math.atan2(x,y))
    return direction 

def getDistance(newLat,newLon,curLat,curLon):

    lat1 = math.radians(curLat)
    lon1 = math.radians(curLon)
    lat2 = math.radians(newLat)
    lon2 = math.radians(newLon)

    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = 6371e3 * c

    return d

def getNewCoords(startLat, startLon, distance, heading):

    lat1 = math.radians(startLat)
    lon1 = math.radians(startLon)
    bearing = math.radians(heading)
    R = 6371e3

    lat2 = math.asin(math.sin(lat1)*math.cos(distance/R) + math.cos(lat1)*math.sin(distance/R)*math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(distance/R) * math.cos(lat1), math.cos(distance/R) - math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return lat2, lon2