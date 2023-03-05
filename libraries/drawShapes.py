import math
import libraries.ssd1306 as ssd1306
from time import sleep
import libraries.planeIcon as planeIcon

def drawcircle(centreX, centreY, radius, oled):

    for i in range(360):
        xCoord = int(centreX + radius*math.cos(math.radians(i)))
        yCoord = int(centreY + radius*math.sin(math.radians(i)))
        oled.pixel(xCoord,yCoord,1)

    #oled.show()


def drawLineAngle(centreX, centreY, radius, angle, oled):
    endX = centreX + radius*math.cos((-angle+90)/360*2*math.pi)
    endY = centreY + radius*math.sin((-angle+90)/360*2*math.pi)

    a = (centreY-endY)/(endX-centreX)
    b = centreY - a*centreX

    for i in range(radius):
        sign = 1
        if centreX > endX:
            sign = -1
        j = abs(centreX-endX)/radius*i
        x = centreX + j*sign
        y = a*x+b
        oled.pixel(int(x), int(y),1)

    #oled.show()

def clearSquare(beginX, endX, beginY, endY, pixelState, oled):
    for i in range(endX-beginX):
        for j in range(endY-beginY):
            oled.pixel(beginX+i,beginY+j,pixelState)
    #oled.show()


def drawIcon(cornerX, cornerY, icon, oled):
    yLen = len(icon)
    xLen = len(icon[0])

    for i in range(xLen):
        for j in range(yLen):
            oled.pixel(cornerX+i,cornerY+j,icon[j][i])

    #oled.show()

def drawIconRotated(cornerX, cornerY, icon, direction, oled):
    yLen = len(icon)
    xLen = len(icon[0])

    if direction == "E":
        for i in range(xLen):
            for j in range(yLen):
                oled.pixel(cornerX+yLen-j,cornerY+i,icon[j][i])

    if direction == "S":
        for i in range(xLen):
            for j in range(yLen):
                oled.pixel(cornerX+i,cornerY+yLen-j,icon[j][i])

    if direction == "W":
        for i in range(xLen):
            for j in range(yLen):
                oled.pixel(cornerX+j,cornerY+i,icon[j][i])

    #oled.show()

def movingIcon_Y(cornerX, startcornerY, endcornerY, icon, speed, oled):
    yLen = len(icon)
    xLen = len(icon[0])

    for a in range(startcornerY-endcornerY):
        drawIcon(cornerX,startcornerY-(a+1),icon,oled)
        oled.show()
        sleep(speed)


def drawAirplane(heading, oled):
    if heading < 23:
        #North
        drawIcon(102,-1,planeIcon.planeIcon_16x16,oled)
        return
    if heading < 45:
        #NorthEast
        drawIcon(102,-1,planeIcon.planeIcon_16x16_r,oled)
        return
    if heading < 68:
        #EastNorth
        drawIconRotated(102,-1,planeIcon.planeIcon_16x16_l,"E",oled)
        return
    if heading < 113:
        #East
        drawIconRotated(102,-1,planeIcon.planeIcon_16x16,"E",oled)
        return
    if heading < 135:
        #EastSouth
        drawIconRotated(102,-1,planeIcon.planeIcon_16x16_r,"E",oled)
        return
    if heading < 158:
        #SouthEast
        drawIconRotated(102,-2,planeIcon.planeIcon_16x16_r,"S",oled) 
        return
    if heading < 203:
        #South
        drawIconRotated(102,-2,planeIcon.planeIcon_16x16,"S",oled) 
        return
    if heading < 225:
        #SouthWest
        drawIconRotated(102,-2,planeIcon.planeIcon_16x16_l,"S",oled) 
        return
    if heading < 248:
        #WestSouth
        drawIconRotated(102,-1,planeIcon.planeIcon_16x16_r,"W",oled)
        return
    if heading < 293:
        #West
        drawIconRotated(102,-1,planeIcon.planeIcon_16x16,"W",oled)
        return
    if heading < 315:
        #WestNorth
        drawIconRotated(102,-1,planeIcon.planeIcon_16x16_l,"W",oled)
        return
    if heading < 338:
        #NorthWest
        drawIcon(102,-1,planeIcon.planeIcon_16x16_l,oled)
        return
    if heading > 337:
        #North
        drawIcon(102,-1,planeIcon.planeIcon_16x16,oled)
        return