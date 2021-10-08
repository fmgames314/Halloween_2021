import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import time
import serial
import threading
import random


def setButtonLED(butLink,buttonID,state):
    serMes = "@LED"+str(buttonID)+"?"+str(state)+"?"
    try:
        butLink.write(str.encode(serMes))
    except:
        print(serMes)


def sendFxSer(fxLink,message):
    try:
        print("Sending "+message)
        fxLink.write( str.encode(message+"\n"))
    except:
        print(message)

def calcualuteCheckSum(message):
    return sum(bytearray(message, encoding="ascii"))
def encodePacket(flag, inData):        
    output = ""
    try:
        output = "@" + flag + "@"
        for param in inData:
            output += str(param) + ","
        checkSum = calcualuteCheckSum(output)
        output += str(checkSum)
    except Exception as e:
        print(e)
    return output

def setFxState(fxLink,device,state):
    state = 1 - state #flip the state here since the relay use inverted logic
    packet = encodePacket("HALRELAY",[device,state])
    sendFxSer(fxLink,packet)

def setRFRelay(fxLink,outletOn,outletOff,state,bitrate,pulse):
    if state == 0:
        packet = encodePacket("RFRELAY",[outletOff,bitrate,pulse])
    if state == 1:
        packet = encodePacket("RFRELAY",[outletOn,bitrate,pulse])
    sendFxSer(fxLink,packet)  


def waitUntilVLCSeconds(speaker, timeInSeconds):
    atTheMark = False
    while atTheMark == False:
        speaker.getPlayerStatus()
        timeIndex = speaker.getPlayTimeSeconds()
        print(timeIndex)
        if timeIndex >= timeInSeconds:
            atTheMark = True
        time.sleep(.2)

    # setRFRelay(self.fxLink,"5248307","5248316", powState, 24, 189 ) ######## group 328-1
    # setRFRelay(self.fxLink,"5248451","5248460", powState, 24, 189 ) ######## group 328-2
    # setRFRelay(self.fxLink,"5248771","5248780", powState, 24, 189 ) ######## group 328-3
    # setRFRelay(self.fxLink,"5250307","5250316", powState, 24, 189 ) ######## group 328-4
    # setRFRelay(self.fxLink,"5256451","5256460", powState, 24, 189 ) ######## group 328-5


class fogFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 8
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

        

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["fogmachine"],1) 
                self.fxState = 2
            # detect turning it off
            if self.fxState == 3:
                setButtonLED(self.butLink,self.effectA_butID,0)
                setFxState(self.fxLink,self.dictOfSerialFX["fogmachine"],0)    
                self.fxState = 0
            time.sleep(.1)                

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 2: # currently fx is on
                self.fxState = 3  # turn off fx
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx


class tazerBoxFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 13
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,1,1) 
                time.sleep(4)
                setFxState(self.fxLink,1,0)
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)                

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx


class trashCanFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 4
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX ,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX


    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["trashMoon"],1)

                setFxState(self.fxLink,self.dictOfSerialFX["trashSpot"],1)
                self.dictOfPlayers["jarSpeaker"].vlcOpenFile(self.dictOfMedia["jarNoise.mp3"])
                time.sleep(10)
                setFxState(self.fxLink,self.dictOfSerialFX["trashSpot"],0)
                setRFRelay(self.fxLink,"5248771","5248780", 1, 24, 189 )
                time.sleep(10)
                setRFRelay(self.fxLink,"5248771","5248780", 0, 24, 189 )

                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx

class zombieFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 9
    effectB_butID = 10 # not using this anymore
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX ,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["picFrameBulb"],0) 
                time.sleep(2)
                setFxState(self.fxLink,self.dictOfSerialFX["FX_ZOMBIE_FAST"],1) 
                time.sleep(.5)
                # self.dictOfPlayers["zomSpeaker"].vlcOpenFile(self.dictOfMedia["outsideZombie2.mp3"])
                setFxState(self.fxLink,self.dictOfSerialFX["zombieRGB"],1) 
                time.sleep(1)
                setFxState(self.fxLink,self.dictOfSerialFX["zombieRGB"],0) 
                time.sleep(3)
                setFxState(self.fxLink,self.dictOfSerialFX["zombieRGB"],1) 
                time.sleep(.6)
                setFxState(self.fxLink,self.dictOfSerialFX["zombieRGB"],0) 
                time.sleep(1.5)
                setFxState(self.fxLink,self.dictOfSerialFX["zombieRGB"],1) 
                time.sleep(.5)
                setFxState(self.fxLink,self.dictOfSerialFX["zombieRGB"],0) 
                time.sleep(1)
                setFxState(self.fxLink,self.dictOfSerialFX["picFrameBulb"],1) 
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # slow effect pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx                  

class spiderDropFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 5
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX ,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                self.dictOfPlayers["spiderSpeaker"].vlcOpenFile(self.dictOfMedia["spider.mp3"])
                setFxState(self.fxLink,19,1) #spider eyes
                time.sleep(1)
                setFxState(self.fxLink,6,1) #spider black light
                time.sleep(1)
                setFxState(self.fxLink,9,1) #spider spotlight
                setFxState(self.fxLink,7,0) #spider pneumatic
                time.sleep(3)
                setFxState(self.fxLink,7,1) #spider pneumatic
                time.sleep(2)
                setFxState(self.fxLink,9,0) #spider spotlight
                setFxState(self.fxLink,6,0) #spider black light
                setFxState(self.fxLink,19,0) #spider eyes
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx


class airSprayerAFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 0
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayA"],1)
                time.sleep(.3)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayA"],0)
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx

class airSprayerBFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 1
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayB"],1)
                time.sleep(.3)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayB"],0)
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx

class airSprayerCFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 2
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayC"],1)
                time.sleep(.3)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayC"],0)
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx
class airSprayerDFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 3
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayD"],1)
                time.sleep(.3)
                setFxState(self.fxLink,self.dictOfSerialFX["ankleSprayD"],0)
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx                                

class mirrorFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 11
    effectB_butID = 12
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                self.dictOfPlayers["mirrorProjector"].vlcOpenFile(self.dictOfMedia["l_Bulb.wav"])
                for i in range(6):
                    setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],1) 
                    time.sleep(.06) 
                    setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],0) 
                    time.sleep(.15+(random.random()/4)) 
                # should play with the bulb going off
                self.dictOfPlayers["mirrorProjector"].vlcOpenFile(self.dictOfMedia["fastMirrorGhost.mp4"])
                time.sleep(.05) 
                waitUntilVLCSeconds(self.dictOfPlayers["mirrorProjector"],1) # delay until video is at 1 seconds
                setRFRelay(self.fxLink,"5248307","5248316", 1, 24, 189 ) #mirror fans //group 328-1
                time.sleep(.6) 
                setFxState(self.fxLink,self.dictOfSerialFX["mirrorRGB"],1) 
                for i in range(3):
                    setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],1) 
                    time.sleep(.1) 
                    setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],0) 
                    time.sleep(1) 
                waitUntilVLCSeconds(self.dictOfPlayers["mirrorProjector"],5) # delay until video is at 5 seconds
                time.sleep(.5) 
                setFxState(self.fxLink,self.dictOfSerialFX["mirrorRGB"],0) 
                time.sleep(.5) 
                setRFRelay(self.fxLink,"5248307","5248316", 0, 24, 189 ) #mirror fans //group 328-1
                time.sleep(2) 
                setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],1) 
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            # this is the old effect that is REALLLY long but its a cool portal
            if self.fxState == 2:
                setButtonLED(self.butLink,self.effectA_butID,1)
                self.dictOfPlayers["mirrorProjector"].vlcOpenFile(self.dictOfMedia["l_Bulb.wav"])
                for i in range(4):
                    setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],1) 
                    time.sleep(.06) 
                    setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],0) 
                    time.sleep(.15+(random.random()/4)) 
                #start portal
                self.dictOfPlayers["mirrorProjector"].vlcOpenFile(self.dictOfMedia["portalChopped.mp4"])
                time.sleep(.5) # maybe stability
                waitUntilVLCSeconds(self.dictOfPlayers["mirrorProjector"],7) # delay until video is at 5 seconds
                setRFRelay(self.fxLink,"5248307","5248316", 1, 24, 189 ) #mirror fans //group 328-1
                time.sleep(1)
                setFxState(self.fxLink,self.dictOfSerialFX["mirrorRGB"],1) 
                waitUntilVLCSeconds(self.dictOfPlayers["mirrorProjector"],28) # delay until video is at 28 seconds
                setRFRelay(self.fxLink,"5248307","5248316", 0, 24, 189 ) #mirror fans //group 328-1
                waitUntilVLCSeconds(self.dictOfPlayers["mirrorProjector"],29) # delay until video is at 29 seconds
                setFxState(self.fxLink,self.dictOfSerialFX["mirrorRGB"],0) 
                time.sleep(3)
                setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],1) 
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            # if self.fxState == 2:
            #     setButtonLED(self.butLink,self.effectB_butID,1)
            #     setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],0) 
            #     time.sleep(1)
            #     self.dictOfPlayers["mirrorProjector"].vlcOpenFile(self.dictOfMedia["headChopped.mov"])
            #     setFxState(self.fxLink,self.dictOfSerialFX["mirrorRGB"],1) 
            #     setRFRelay(self.fxLink,"5248307","5248316", 1, 24, 189 ) #mirror fans ON //group 328-1
            #     waitUntilVLCSeconds(self.dictOfPlayers["mirrorProjector"],15) # delay until video is at 12 seconds
            #     setRFRelay(self.fxLink,"5248307","5248316", 0, 24, 189 ) #mirror fans OFF //group 328-1
            #     setFxState(self.fxLink,self.dictOfSerialFX["mirrorRGB"],0) 
            #     time.sleep(1)
            #     setFxState(self.fxLink,self.dictOfSerialFX["mirrorBulb"],1) 
            #     setButtonLED(self.butLink,self.effectB_butID,0)
            #     self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx
        if buttonID == self.effectB_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 2  # turn on fx




class pictureFrameFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 15
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                setFxState(self.fxLink,self.dictOfSerialFX["picFrameBulb"],1) 
                self.dictOfPlayers["pictureScreen"].vlcSeek(0)
                time.sleep(.1) # maybe stability
                self.dictOfPlayers["pictureScreen"].vlcPlay()
                waitUntilVLCSeconds(self.dictOfPlayers["pictureScreen"],10) # delay until video is at 5 seconds
                self.dictOfPlayers["pictureScreen"].vlcPause()
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx             



class ambientSpiderFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 7
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            while self.fxState == 1:
                self.dictOfPlayers["ambientSpider"].vlcOpenFile(self.dictOfMedia["bubblingcauldron.mp3"])
                waitUntilVLCSeconds(self.dictOfPlayers["ambientSpider"],58)
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0:
                self.fxState = 1
                setButtonLED(self.butLink,self.effectA_butID,1)
            else:
                self.fxState = 0
                setButtonLED(self.butLink,self.effectA_butID,0)      





class eyeballFX:
    # variables
    progWorking = True
    fxState = 0
    effectA_butID = 14
    dictOfPlayers = {}
    dictOfMedia = {}
    dictOfSerialFX = {}
    butLink = None
    fxLink = None

    def __init__(self,speakers,media,serialFX,fxLink,butLink):
        threading.Thread(target=self.loopThread, args=()).start()
        self.fxLink = fxLink
        self.butLink = butLink
        self.dictOfPlayers = speakers
        self.dictOfMedia = media
        self.dictOfSerialFX = serialFX

    def loopThread(self):
        while self.progWorking == True:
            #loop starts here
            if self.fxState == 1:
                setButtonLED(self.butLink,self.effectA_butID,1)
                # start fx
                self.dictOfPlayers["topSpeaker"].vlcOpenFile(self.dictOfMedia["flameAndEyeball.mp3"])
                time.sleep(.3)
                setFxState(self.fxLink,17,1) #candelobras on
                time.sleep(2)
                setFxState(self.fxLink,16,1) #eyeball on
                time.sleep(5)
                setFxState(self.fxLink,16,0) #eyeball off
                setButtonLED(self.butLink,self.effectA_butID,0)
                self.fxState = 0
                time.sleep(3)
                setFxState(self.fxLink,17,0) #candelobras off
            time.sleep(.1)

    def arcadeButtonPressed(self,buttonID):
        if buttonID == self.effectA_butID: # button pressed
            if self.fxState == 0: # currently fx is off
                self.fxState = 1  # turn on fx     