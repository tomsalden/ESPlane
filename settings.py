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
areaMaxLat = 54.2
areaMinLat = 50
areaMaxLon = 10
areaMinLon = 1.5

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
                      "CHAOS","MOOSE","WOLF","SNAKE",
                      "CEF","NOBLE","ROGUE","SVF"]

importantAiplaneModels = ["C17","R135","A400","C30J",
                          "A124","EUFI","C130","H47",
                          "F35","K35R","HAWK","P8",
                          "C5M"]

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

servoEnabled = False

led = machine.Pin(IndicatorLED, machine.Pin.OUT)

notificationAltitude = 10
#startupSound = '1 G7 0.5 43;0 C7 0.5 43'
startupSound = '0 D#6 1 14;2.999999999999999 D6 1 14;3.999999999999999 C#6 1 14;5.999999999999999 F#5 1 14;6.999999999999999 D#5 1 14;7.999999999999999 C#5 1 14;9 C5 1 14;10 C5 1 14'
notificationSound = '1 G7 0.5 43;0 C7 0.5 43'

#############   Program variables       #############
oledConnected = False

main_updateTime = 0
thread_OLED_updateTime = 0
thread_Servo_updateTime = 0
thread_Plane_updateTime = 0
thread_location_updateTime = 0

main_timeout = 15
thread_OLED_timeout = 10
thread_Servo_timeout = 10
thread_Plane_timeout = 30
thread_location_timeout = 10

thread_Plane_stopsignal = True
thread_Plane_stopped = True
thread_Plane_forceStop = False

planes = classes.selectedPlanes(0,0,0,0,0,0,0,0,0,0)
planesReady = False
currentPlane = classes.selectedPlanes(0,0,0,0,0,0,0,0,0,0)
selectedPlane = 0
selectedPlaneName = ""
notified = False        #Check if a notification has been made for the current airplane
airplanesUpdated = False

geomatics = classes.updatedGeomatis(0,0,0)
geomaticsReady = False

networkConnection = False
