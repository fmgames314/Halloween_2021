import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import time
import serial
#import other python files
from fxThreads import *    
import os
import threading


class vlcPlayer:
    # variables
    ip = ""
    port = ""
    password = ""
    length = 0
    time = 0
    state = ""


    def __init__(self,ip,port,password):
        self.ip = ip
        self.port = port
        self.password = password

    # Orientation
    def getPlayerStatus(self):
        vlcHttpResponse = requests.get('http://'+str(self.ip)+':'+str(self.port)+'/requests/status.xml?', verify=False, auth=HTTPBasicAuth('', self.password))
        self.parseVlcXml(vlcHttpResponse.content)

    def parseVlcXml(self,statusXML):
        statusDict = xmltodict.parse(statusXML,process_namespaces=True)
        self.length = statusDict["root"]["length"]
        self.state = statusDict["root"]["state"]
        try:
            self.time = int(statusDict["root"]["time"])
        except:
            print("couldn't convert vlc time to int")
        

    def getPlayTimeSeconds(self):
        return self.time

    def vlcOpenFile(self,path):
        URL = 'http://'+str(self.ip)+':'+str(self.port)+'/requests/status.xml?command=in_play&input='+path+''
        vlcHttpResponse = requests.get(URL, verify=False, auth=HTTPBasicAuth('', self.password))
        self.parseVlcXml(vlcHttpResponse.content)

    def vlcStop(self):
        URL = 'http://'+str(self.ip)+':'+str(self.port)+'/requests/status.xml?command=pl_stop'
        vlcHttpResponse = requests.get(URL, verify=False, auth=HTTPBasicAuth('', self.password))
        self.parseVlcXml(vlcHttpResponse.content)

    def vlcPause(self):
        URL = 'http://'+str(self.ip)+':'+str(self.port)+'/requests/status.xml?command=pl_pause'
        vlcHttpResponse = requests.get(URL, verify=False, auth=HTTPBasicAuth('', self.password))
        self.parseVlcXml(vlcHttpResponse.content)
        if self.state != "paused":
            print("not paused, trying again")
            self.vlcPause()

    def vlcPlay(self):
        URL = 'http://'+str(self.ip)+':'+str(self.port)+'/requests/status.xml?command=pl_play'
        vlcHttpResponse = requests.get(URL, verify=False, auth=HTTPBasicAuth('', self.password))
        self.parseVlcXml(vlcHttpResponse.content)
        if self.state != "playing":
            print("not playing, trying again")
            self.vlcPlay()
    def vlcSeek(self,seconds):
        URL = 'http://'+str(self.ip)+':'+str(self.port)+'/requests/status.xml?command=seek&val='+str(seconds)+''
        vlcHttpResponse = requests.get(URL, verify=False, auth=HTTPBasicAuth('', self.password))
        self.parseVlcXml(vlcHttpResponse.content)



#locate all media files into a dictionary
path = 'C:\\halloween\\ProgramMedia'
dictOfMedia = {}
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        dictOfMedia[file] = os.path.join(r, file)
print("List of media files size: ",len(dictOfMedia))

#setup serial to master arduino
masterArduinoConnected = False
try:
    fxLink = serial.Serial("COM7", 9600)
    masterArduinoConnected = True
except:
    print("Couldn't connect to master arduino")
    raise SystemExit


#setup serial to button box
readButtonSerial = False
try:
    butLink = serial.Serial("COM3", 9600)
    readButtonSerial = True
except:
    print("Couldn't connect to button arduino")
    raise SystemExit

numberOfButts = 16
deviceMode = [0] * numberOfButts
#declare VLC objects
dictOfPlayers = {
    "topSpeaker": vlcPlayer("127.0.0.1","6100","meatball"),
    "jarSpeaker": vlcPlayer("127.0.0.1","6101","meatball"),
    "spiderSpeaker": vlcPlayer("127.0.0.1","6102","meatball"),
    "zomSpeaker": vlcPlayer("127.0.0.1","6103","meatball"),
    "mirrorProjector": vlcPlayer("127.0.0.1","6104","meatball"),
    "pictureScreen": vlcPlayer("127.0.0.1","6105","meatball"),
    "ambientSpider": vlcPlayer("127.0.0.1","6106","meatball")
}
dictOfSerialFX = {
    "ACrelay_1":0,
    "ACrelay_2":1,
    "ACrelay_3":2,
    "ACrelay_4":3,
    "relay_1":4,
    "mirrorBulb":5,
    "mirrorRGB":6,
    "relay_4":7,
    "picFrameBulb":8,
    "zombieRGB":9,
    "trashMoon":10,
    "trashSpot":11,
    "ankleSprayD":12,
    "ankleSprayC":13,
    "ankleSprayB":14,
    "ankleSprayA":15,
    "relay_13":16,
    "relay_14":17,
    "fogmachine":18,
    "blackLight":19,
    "FX_ZOMBIE_SLOW":100,
    "FX_ZOMBIE_FAST":101,

}

# byte breakerBox = relay_13;
# byte spiderPneumatic = relay_8;
# byte spiderSpotlight = relay_7;
# byte ankleSprayA = relay_12;
# byte ankleSprayB = relay_11;
# byte ankleSprayC = relay_10;
# byte ankleSprayD = relay_9;
# byte jarHead = ACrelay_1;
# byte blackLight = relay_16;
# byte mirrorFans = ACrelay_2;
# byte mirrorLights = relay_2;
# byte mirrorBulb = relay_5;
# byte fogMachine = relay_15;
# byte eyeball = relay_4;
# byte candleLamps = relay_3;
# byte pathLEDstrip = ACrelay_3;

#FX assets creation and organization
listOfFX = []
listOfFX.append( tazerBoxFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( trashCanFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( mirrorFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( spiderDropFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( airSprayerAFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( airSprayerBFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( airSprayerCFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( airSprayerDFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( fogFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( zombieFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( pictureFrameFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( ambientSpiderFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )
listOfFX.append( eyeballFX(dictOfPlayers,dictOfMedia,dictOfSerialFX,fxLink,butLink) )

#setup extra monitors with video VLCs
dictOfPlayers["pictureScreen"].vlcOpenFile(dictOfMedia["pictureFrameB.mp4"])
time.sleep(.5)
dictOfPlayers["pictureScreen"].vlcSeek(10)
time.sleep(.5)
dictOfPlayers["pictureScreen"].vlcPause()
# now the mirror
dictOfPlayers["mirrorProjector"].vlcOpenFile(dictOfMedia["headChopped.mov"])
time.sleep(.2)
dictOfPlayers["mirrorProjector"].vlcPause()




print("List of FX size: ",len(listOfFX))

# read the button states and report them to threads
while readButtonSerial == True:
     cc=(butLink.readline()).decode("utf-8").rstrip() 
     ccParams = cc.split(",")
     command = ccParams[0]
     buttonID = int(ccParams[1])
     if command == "P":
        print("Button "+str(buttonID)+" pressed")  
        for fx in listOfFX:
            fx.arcadeButtonPressed(buttonID)
     if command == "R":
        pass
        print("Button "+str(buttonID)+" Released")  
    
fellBack = True
text = input("Enter button ID to simulate: ")
while fellBack == True:
    text = input("")
    if text != "":
        buttonID = int(text)
        for fx in listOfFX:
            fx.arcadeButtonPressed(buttonID)

# device states on arduino
# 1 = tazer box
# 2 = headJar power relay
# 3 = bulb over mirror
# 4 = mirror color lights
# 5 = mirror fans power relay
# 6 = spider black light
# 7 = spider pneumatic
# 8 = fog machine
# 9 = spider spotlight
# 10 = AirSprayerA
# 11 = AirSprayerB
# 12 = AirSprayerC
# 13 = AirSprayerD
# 14 = zombieSlow
# 15 = zombieFast
# 16 = eyeball
# 17 = candle lamps
# 18 = pathLEDstrip
# 19 = spiderEyes

###########Example code###############
# #setup VLC connection
# frontSpeaker = vlcPlayer("127.0.0.1","6100","meatball")
# #play a file
# frontSpeaker.vlcOpenFile('C:\\test\\video.mp4')
# time.sleep(2)
# frontSpeaker.vlcPause()
# time.sleep(2)
# frontSpeaker.vlcSeek(8)
# frontSpeaker.vlcPlay()
# # time.sleep(2)
# # frontSpeaker.vlcPause()
# timeIndex = frontSpeaker.getPlayTimeSeconds()
# print(timeIndex)
