import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import time


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
        self.time = statusDict["root"]["time"]
        self.state = statusDict["root"]["state"]

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



#setup VLC connection
frontSpeaker = vlcPlayer("127.0.0.1","6100","meatball")
#play a file
frontSpeaker.vlcOpenFile('C:\\test\\video.mp4')
time.sleep(2)
frontSpeaker.vlcPause()
time.sleep(2)
frontSpeaker.vlcSeek(8)
frontSpeaker.vlcPlay()
# time.sleep(2)
# frontSpeaker.vlcPause()
timeIndex = frontSpeaker.getPlayTimeSeconds()
print(timeIndex)