import machine
import classes

#############   Pin Assignments       #############
dirServoPin = 25
altServoPin = 33

I2C_SDA = 21
I2C_SCL = 22

IndicatorLED = 2

#############   Variables       #############
## Coordinates
# Search area settings
areaMaxLat = 55.5007
areaMinLat = 50.0000
areaMaxLon = 7.6836
areaMinLon = 0.6271

# Current coordinates
myLat = 52.1918766
myLon = 4.7530688
myAlt = 0

#Parameters for area divisions, so not all planes have to be handled at once
areaDivisions = 1       #Default settings
maxAreaDivisions = 10    #Maximum divisions

## Callsigns to look out for
importantAirplanes = ["RCH","LAGR","RRR","NCHO",
                      "MMF","NAF","NATO","RED",
                      "HKY","QID","CFC","JAKE",
                      "ASCOT","HOBO","BART","BLKCAT",
                      "OMEN","BLUE","BGA","ZXP",
                      "DGLBA","LIFE","ZXP","BAF",
                      "CHAOS","MOOSE","WOLF","RYR7BH"]

#Servo maximum values
# minDirValue = 18
# maxDirValue = 120
# minDirValue = int(minDirValue / 1023 * 65535)
# maxDirValue = int(maxDirValue / 1023 * 65535)

minDirValue = 1153
maxDirValue = 7687

# minAltValue = 30
# maxAltValue = 140
# minAltValue = int(minAltValue / 1023 * 65535)
# maxAltValue = int(maxAltValue / 1023 * 65535)

minAltValue = 1922
maxAltValue = 8969

led = machine.Pin(IndicatorLED, machine.Pin.OUT)


#############   Program variables       #############
oledConnected = False

main_updateTime = 0
thread_OLED_updateTime = 0
thread_Servo_updateTime = 0
thread_Plane_updateTime = 0
thread_location_updateTime = 0

main_timeout = 5
thread_OLED_timeout = 10
thread_Servo_timeout = 10
thread_Plane_timeout = 30
thread_location_timeout = 10

thread_Plane_stopsignal = True
thread_Plane_stopped = True

planes = classes.selectedPlanes(0,0,0,0,0,0,0,0,0,0)
planesReady = False
currentPlane = classes.selectedPlanes(0,0,0,0,0,0,0,0,0,0)
selectedPlane = 0

geomatics = classes.updatedGeomatis(0,0,0)
geomaticsReady = False
