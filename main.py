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

# Make buzzer sound
song = '0 A#3 1 0;0 F#3 2 0;1 C#4 1 0;2 C4 1 0;3 C#4 1 0;4 A#3 1 0;6 A#3 1 0;6 F#3 2 0;7 C4 1 0;8 C#4 1 0;9 G#4 1 0;10 F4 1 0;12 A#3 1 0;12 F#3 2 0;13 C#4 1 0;14 C4 1 0;15 C#4 1 0;16 A#3 1 0;18 A#3 1 0;18 F#3 2 0;19 C4 1 0;20 C#4 1 0;21 G#4 1 0;22 F4 1 0;24 A#3 1 0;24 F3 2 0;25 C#4 1 0;26 C4 1 0;27 C#4 1 0;28 A#3 1 0;30 A#3 1 0;31 C4 1 0;30 F3 2 0;32 C#4 1 0;33 G#4 1 0;34 F4 1 0;36 F3 2 0;36 D#5 2 0;38 C6 2 0;38 G#3 2 0;40 C4 2 0;40 A#5 2 0;42 G#5 1 0;42 D#4 2 0;43 F#5 1 0;44 C4 1 0;45 G#3 1 0;44 F5 2 0;46 D#4 1 0;47 C4 1 0;46 G#5 2 0;48 A#3 1 0;48 F#3 2 0;49 C#4 1 0;50 C4 1 0;51 C#4 1 0;52 A#3 1 0;54 A#3 1 0;55 C4 1 0;54 F#3 2 0;56 C#4 1 0;57 G#4 1 0;58 F4 1 0;60 A#3 1 0;60 F#3 2 0;61 C#4 1 0;48 A#5 15 0;62 C4 1 0;63 C#4 1 0;64 A#3 1 0;66 A#3 1 0;66 F#3 2 0;67 C4 1 0;68 C#4 1 0;69 G#4 1 0;70 F4 1 0;72 A#3 1 0;72 F3 2 0;73 C#4 1 0;74 C4 1 0;75 C#4 1 0;76 A#3 1 0;78 A#3 1 0;78 F3 2 0;79 C4 1 0;80 C#4 1 0;81 G#4 1 0;82 F4 1 0;84 D#5 2 0;84 D#6 2 0;84 G#3 2 0;86 C7 2 0;86 D#3 2 0;86 C6 2 0;88 A#6 2 0;88 F3 2 0;88 A#5 2 0;90 G#5 1 0;90 G#6 1 0;90 G#3 2 0;91 F#6 1 0;91 F#5 1 0;92 F5 2 0;92 C4 2 0;92 F6 2 0;94 D#4 2 0;94 G#6 2 0;94 G#5 2 0;96 F#3 2 0;98 C4 1 0;99 C#4 1 0;100 A#3 1 0;101 F3 1 0;96 A#5 8 0;102 F#3 2 0;104 C4 1 0;104 F5 2 0;105 C#4 1 0;106 A#3 1 0;106 G#5 2 0;107 D#4 1 0;108 G#3 2 0;110 D#3 1 0;108 A#5 4 0;111 F3 1 0;112 G#3 1 0;112 C#6 2 0;113 F3 1 0;114 D#6 1 0;114 D#3 2 0;115 C#6 1 0;116 F3 2 0;116 C6 2 0;118 G#3 2 0;118 C#6 2 0;120 A#3 1 0;121 A#4 1 0;122 D#4 1 0;123 F4 1 0;124 C#4 1 0;125 G#3 1 0;126 A#3 1 0;127 A#4 1 0;128 D#4 1 0;129 F4 1 0;130 C#4 1 0;131 G#3 1 0;132 A#3 1 0;133 A#4 1 0;120 A#5 15 0;134 D#4 1 0;135 F4 1 0;136 C#4 1 0;137 F3 1 0;138 G#3 2 0;140 D#3 2 0;142 G#3 2 0;144 A#4 1 0;144 A#3 1 0;144 F#3 1 0;145 C#5 1 0;145 C#4 1 0;146 C5 1 0;146 C4 1 0;147 C#5 1 0;147 C#4 1 0;148 A#4 1 0;148 A#3 1 0;150 A#4 1 0;150 F#3 1 0;150 A#3 1 0;151 C4 1 0;151 C5 1 0;152 C#4 1 0;152 C#5 1 0;153 G#4 1 0;154 F4 1 0;154 F5 1 0;156 A#4 1 0;156 A#3 1 0;156 F#3 1 0;157 C#5 1 0;157 C#4 1 0;158 C5 1 0;158 C4 1 0;159 C#5 1 0;159 C#4 1 0;160 A#3 1 0;160 A#4 1 0;162 A#4 1 0;162 A#3 1 0;162 F#3 1 0;163 C5 1 0;163 C4 1 0;164 C#5 1 0;164 C#4 1 0;165 G#4 1 0;166 F5 1 0;166 F4 1 0;168 A#3 1 0;168 F3 1 0;168 A#4 1 0;169 C#5 1 0;169 C#4 1 0;170 C5 1 0;170 C4 1 0;171 C#4 1 0;171 C#5 1 0;172 A#3 1 0;172 A#4 1 0;174 A#4 1 0;174 A#3 1 0;174 F3 1 0;175 C5 1 0;175 C4 1 0;176 C#5 1 0;176 C#4 1 0;177 G#4 1 0;178 F4 1 0;178 F5 1 0;180 F3 2 0;180 D#6 2 0;180 F4 2 0;182 G#4 2 0;182 C7 2 0;182 G#3 2 0;184 C4 2 0;184 A#6 2 0;184 C5 2 0;186 G#6 1 0;186 D#5 2 0;186 D#4 2 0;187 F#6 1 0;188 C5 1 0;188 C4 1 0;189 G#3 1 0;189 G#4 1 0;188 F6 2 0;190 D#4 1 0;190 D#5 1 0;191 C5 1 0;190 G#6 2 0;191 C4 1 0;192 A#4 1 0;192 A#3 1 0;192 F#3 1 0;193 C#5 1 0;193 C#4 1 0;194 C4 1 0;194 C5 1 0;195 C#4 1 0;195 C#5 1 0;196 A#4 1 0;196 A#3 1 0;198 F#3 1 0;198 A#3 1 0;198 A#4 1 0;199 C5 1 0;199 C4 1 0;200 C#4 1 0;200 C#5 1 0;201 G#4 1 0;202 F4 1 0;202 F5 1 0;204 A#4 1 0;204 F#3 1 0;204 A#3 1 0;205 C#4 1 0;205 C#5 1 0;206 C5 1 0;192 A#6 15 0;206 C4 1 0;207 C#4 1 0;207 C#5 1 0;208 A#3 1 0;208 A#4 1 0'
song = '0 C6 1 43;0.9009733991272968 F#6 1 43 0.8329831064078411'
song = '2 C7 2 43;0 C6 1 43;1 G6 1 43 0.8329831064078411'
song = '1 G7 0.5 43;0 C7 0.5 43'
#song = '10.25 C#7 0.25 43;0 G7 0.5 43;1 G7 2 43;5.75 C#7 0.25 43;7.25 B6 0.25 43;8.25 F#7 0.25 43;4.75 C7 0.25 43;6.5 E7 0.25 43;9.5 A#6 0.25 43;11 E7 0.25 43;9.75 D#7 0.25 43;8 C7 0.25 43'

#https://onlinesequencer.net/

mySong = music(song, pins=[machine.Pin(4)], looping=False)

while mySong.stopped == False:
    mySong.tick()
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
