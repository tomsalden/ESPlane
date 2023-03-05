#############   Control all servo information   #############
import machine
import time

import settings

#Initialise servos
def initServos():
    global dirServo
    global altServo

    dirServoPinObj = machine.Pin(settings.dirServoPin, machine.Pin.OUT)
    altServoPinObj = machine.Pin(settings.altServoPin, machine.Pin.OUT)

    dirServo = machine.PWM(dirServoPinObj)
    altServo = machine.PWM(altServoPinObj)

    dirServo.init(freq=50,duty_u16=6406)
    altServo.init(freq=50,duty_u16=6406)

    # dirServo.freq(50)
    # altServo.freq(50)
    # altServo.duty_u16(6406)
    # dirServo.duty_u16(6406)

def updateServos():
    previousAlt = 0
    previousDir = 0
    noChangeDir = 0
    noChangeAlt = 0
    while settings.main_updateTime + settings.main_timeout > time.time():
        settings.thread_Servo_updateTime = time.time()
        time.sleep(1)

        #Check if movement information can be accessed
        if not settings.geomaticsReady:
            continue

        #Check if there are any planes at all
        if not settings.planes.name:
            # print("No airplanes available, servos not active")
            dirServo.deinit()
            altServo.deinit()
            continue

        if previousAlt == settings.geomatics.altAngle:
            noChangeAlt = noChangeAlt + 1
        else:
            noChangeAlt = 0

        if  previousDir == settings.geomatics.dirAngle:
            noChangeDir = noChangeDir + 1
        else:
            noChangedir = 0

        if noChangeAlt > 5:
            altServo.deinit()

        previousAlt = settings.geomatics.altAngle
        previousDir = settings.geomatics.dirAngle
            
        #Set the correct position of the servos
        servoController(settings.minAltValue,settings.maxAltValue,settings.minDirValue,settings.maxDirValue,settings.geomatics.altAngle,settings.geomatics.dirAngle)
    dirServo.deinit()
    altServo.deinit()
    print("Servo manager has been shut down")



def arduinoMap(x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def servoController(minAlt, maxAlt, minDir, maxDir ,altAngle, dirAngle):
    altCenter = maxAlt - (maxAlt - minAlt)/2
    #print("Direction: ", dirAngle, ", Altitude: ", altAngle)
    if (dirAngle > 0):
        dirServoDuty = int(arduinoMap(dirAngle, 0, 180, maxDir, minDir))
        altServoDuty = int(arduinoMap(altAngle, 0, 90, minAlt, altCenter))

        dirServo.init(freq=50,duty_u16=dirServoDuty)
        altServo.init(freq=50,duty_u16=altServoDuty)
        # dirServo.duty_u16(dirServoDuty)
        # altServo.duty_u16(altServoDuty)

        # print(dirServoDuty)
        # print(altServoDuty)
        return
    
    dirServoDuty = int(arduinoMap(dirAngle, 0, -180, minDir, maxDir))
    altServoDuty = int(arduinoMap(altAngle, 0, 90, maxAlt, altCenter))

    #print(dirServoDuty)
    #print(altServoDuty)     
    
    dirServo.init(freq=50,duty_u16=dirServoDuty)    
    altServo.init(freq=50,duty_u16=altServoDuty)
    # dirServo.duty_u16(dirServoDuty)
    # altServo.duty_u16(altServoDuty)
