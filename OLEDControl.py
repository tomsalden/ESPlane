#############   Control the OLED   #############
import machine
import time
import math
import libraries.ssd1306 as ssd1306
import libraries.drawShapes as drawShapes
import libraries.planeIcon as planeIcon

import settings

noPlanesFound = 0

#Initialise OLED
def initOLED():
    global oled
    global oled_width
    global oled_height

    i2c = machine.SoftI2C(scl=machine.Pin(settings.I2C_SCL), sda=machine.Pin(settings.I2C_SDA))
    oled_width = 128
    oled_height = 64

    try:
        oled = ssd1306.SSD1306_I2C(oled_width,oled_height,i2c)

        oled.fill(0)
        oled.text('ESPAim', 0, 0)
        oled.text('Initialising', 0, 20)
        oled.text('Connecting to', 0, 40)
        oled.text('network...',0,50)
                
        oled.show()
        settings.oledConnected = True
    except OSError as e:
        print("No connection to the OLED display. Following error occured:")
        print(e)
        settings.oledConnected = False

def networkConnected():
    oled.fill(0)
    oled.text('ESPAim', 0, 0)
    oled.text('Connected!', 0, 20)
    oled.text('Searching!', 0, 40)  
    oled.show()

    drawShapes.movingIcon_Y(102,64,-1,planeIcon.planeIcon_16x16,0.01,oled)

def noPlanesOLED():
    global noPlanesFound
    noPlanesFound = noPlanesFound + 1
    if noPlanesFound > 5:
        oled.poweroff()
    oled.fill(0)
    oled.text('No planes', 0, 0)
    oled.text('found!!', 0, 20)
    oled.text('Retrying...', 0, 40)
    oled.show()

        
def updateOLED():
    global noPlanesFound
    while settings.main_updateTime + settings.main_timeout > time.time():
        settings.thread_OLED_updateTime = time.time()
        time.sleep(1)

        #Check if plane information can be accessed
        if not settings.planesReady:
            continue

        #Check if there are any planes at all
        if not settings.planes.name:
            print("No planes found")
            noPlanesOLED()
            drawShapes.movingIcon_Y(102,64,-20,planeIcon.planeIcon_16x16,0.005,oled)
            continue

        #Check if movement information can be accessed
        if not settings.geomaticsReady:
            continue

        #Show the information if there are any planes
        if noPlanesFound > 5:
            noPlanesFound = 0
            oled.poweron()
            oled.init_display()
        
        #Setup OLED screen with the information
        firstLineText = str(settings.currentPlane.name)
        secondLineText = str('Type: ' + settings.currentPlane.type)
        thirdLineText = str('Reg.: ' + settings.currentPlane.registration)
        fourthLineText = str('Dist: ' + str(math.ceil(settings.geomatics.distance/1000)) + 'km')
        fifthLineText = str('Alt: ' + str(int(settings.currentPlane.altitude/3.28084)) + 'm')
        sixthLineText = str('Spd: ' + str(int(settings.currentPlane.speed*1.852)) + 'km/h')

        drawShapes.clearSquare(0,oled_width,0,oled_height,0,oled)
        oled.text(firstLineText, 0, 5)
        oled.text(secondLineText, 0, 16)
        oled.text(thirdLineText, 0, 26)
        oled.text(fourthLineText, 0, 36)
        oled.text(fifthLineText, 0, 46)
        oled.text(sixthLineText, 0, 56)

        drawShapes.drawcircle(118,50,10,oled)
        drawShapes.drawLineAngle(118,50,13,settings.geomatics.dirAngle,oled)

        drawShapes.drawAirplane(settings.currentPlane.heading,oled)

        # if settings.currentPlane.heading < 45 or settings.currentPlane.heading > 314:
        #     #Heading is to the north
        #     drawShapes.drawIcon(102,-1,planeIcon.planeIcon_16x16,oled)
        # if settings.currentPlane.heading > 44 and settings.currentPlane.heading < 135:
        #     #Heading is to the east
        #     drawShapes.drawIconRotated(102,-1,planeIcon.planeIcon_16x16,"E",oled)
        # if settings.currentPlane.heading > 134 and settings.currentPlane.heading < 225:
        #     #Heading is to the south
        #     drawShapes.drawIconRotated(102,-2,planeIcon.planeIcon_16x16,"S",oled) 
        # if settings.currentPlane.heading > 224 and settings.currentPlane.heading < 315:
        #     #Heading is to the east
        #     drawShapes.drawIconRotated(102,-1,planeIcon.planeIcon_16x16,"W",oled)

        #Check if there is more than one plane
        amountPlanes = len(settings.planes.name)
        if amountPlanes > 1 and amountPlanes < 10:
            #drawShapes.clearSquare(80,82,7,9,1,oled)
            oled.text(str(len(settings.planes.name)),85,5)

        if amountPlanes > 9:
            #drawShapes.clearSquare(80,82,7,9,1,oled)
            oled.text(str(len(settings.planes.name)),80,5)

        oled.show()
    
    oled.poweroff()
    print("OLED manager has been shut down")


