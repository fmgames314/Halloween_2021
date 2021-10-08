#include <SoftwareSerial.h>
SoftwareSerial mp3Trigger(2, 3); // RX, TX

#include <Servo.h>

Servo head;
byte headPin = 9;

byte relayA = 10;
byte relayB = 11;
byte relayC = 12;
byte relayD = 6;

void setup() {
  Serial.begin(9600);
  mp3Trigger.begin(38400);
  pinMode(relayA,OUTPUT);
  pinMode(relayB,OUTPUT);
  pinMode(relayC,OUTPUT);
  pinMode(relayD,OUTPUT);
  digitalWrite(relayA,HIGH); // remember these relays turn off when HIGH and on when LOW
  digitalWrite(relayB,HIGH);
  digitalWrite(relayC,HIGH);
  digitalWrite(relayD,HIGH);
  //servo for head
  pinMode(headPin,OUTPUT);
  head.attach(headPin);
  head.write(160);
  delay(1000);
  head.detach();
  mp3Trigger.write('T'); mp3Trigger.write("1");
//analogWrite(9,127);
  
}
//570 2400
byte armA = relayC;
byte armB = relayD;
byte lightA = relayA;
byte lightB = relayB;

//move modes
byte slowMove = 0;
byte fastMove = 0;
//FX variables
int headPos = 0;

//loop start
void loop() {
    String incomingPacket = Serial.readStringUntil('\n'); 
    byte packetStatus = processIncomingPacket(incomingPacket);
    // use packetStatus to check if packet had good or bad checksum
    if(packetStatus == 1){
      Serial.println("Good Checksum");
    }
    else{
      Serial.println("BAD Checksum!");
    }
  //fast movment
  if(fastMove == 1){
    mp3Trigger.write('T'); mp3Trigger.write("2"); // zombie
    digitalWrite(lightA,LOW); //actually on
    headPos = 110;
    head.attach(headPin);
    delay(50);
    head.write(headPos);
    for(int i = 0; i < 2; i+=1){
      setArms(1,0);
      delay(500);
      setArms(0,0);
      delay(1000);
      digitalWrite(lightB,LOW); //actually on
      setArms(0,1);
      delay(500);
      setArms(0,0);
      digitalWrite(lightB,HIGH); //actually off
      delay(1000);
    }
    headPos = 80;
    head.write(headPos);
    mp3Trigger.write('T'); mp3Trigger.write("3"); // zombie higher pitch
    for(int i = 0; i < 2; i+=1){
      setArms(1,0);
      digitalWrite(lightB,LOW); //actually on
      delay(600);
      setArms(0,1);
      digitalWrite(lightB,HIGH); //actually off
      delay(600);
      head.write(headPos);
      headPos+=30;
    }  
    setArms(0,0);
    delay(800);
    digitalWrite(lightB,LOW); //actually on
    setArms(1,1);
    delay(700);  
    digitalWrite(lightB,HIGH); //actually off
    delay(80); 
    setArms(0,0);
    delay(80); 
    fastMove = 0;
    headPos = 160;
    head.write(headPos);
    delay(80); 
    digitalWrite(lightA,HIGH); //actually off
    delay(500);
    head.detach();
  }
  
  //slow movement
  if(slowMove == 1){
    digitalWrite(lightA,LOW); //actually on
    headPos-=1;
    head.write(headPos);
    delay(25);
    if(headPos < 30){
      slowMove = 2;
    }
  }
  if(slowMove == 2){
    delay(1000);
    headPos = 170;
    head.write(headPos);
    slowMove = 0;
    digitalWrite(lightA,HIGH); //actually off
    delay(700);
    head.detach();
  }
    
}


void setArms(byte left, byte right){
  digitalWrite(armA,!left);
  digitalWrite(armB,!right);
}




void powerDevice(int deviceNum, byte state)
{
  if(deviceNum == 100 && state == 0){ // use inverted logic since all the actual relays too. 
    //slow movement start
    if(slowMove == 0){
      head.attach(headPin);
      delay(50);
      headPos = 160;
      slowMove = 1;
    }
  }
  if(deviceNum == 101 && state == 0){ // use inverted logic since all the actual relays too.
    //fast movement start
    if(fastMove == 0){
      fastMove = 1;
    }
  }  
}



//---------------------------------------------------------///
//---------------------SENDING PACKET----------------------///
//---------------------------------------------------------///
String output_packet = "";
void addToPacket(float data){
  output_packet+=String(data,2)+",";
}
void addToPacket(double data){
  output_packet+=String(data,2)+",";
}
void addToPacket(long data){
  output_packet+=String(data)+",";
}
void addToPacket(int data){
  output_packet+=String(data)+",";
}
void addToPacket(String data){
  output_packet+=data+",";
}
void clearPacket(){
  output_packet = "";
}
String getPacket(String flag){
  output_packet = "@"+flag+"@"+output_packet;
  long checkSum = checkSumFromString(output_packet);
  output_packet += String(checkSum);
  return output_packet+"\n";
}

long checkSumFromString(String inputString){
  long sum = 0;
  for(byte b=0; b<inputString.length(); b++)
  {
     sum += inputString[b];
  }
  return sum;
}
//---------------------------------------------------------///
//---------------------Recieving PACKET----------------------///
//---------------------------------------------------------///
String midString(String str, String start, String finish){
  int locStart = str.indexOf(start);
  if (locStart==-1) return "";
  locStart += start.length();
  int locFinish = str.indexOf(finish, locStart);
  if (locFinish==-1) return "";
  return str.substring(locStart, locFinish);
}


byte checkPacketHealth(String packet){
  int lastCommaPos = packet.lastIndexOf(",");
  unsigned long checkSum = (packet.substring(lastCommaPos+1)).toInt();
  String packetWithNoCheckSum = packet.substring(0,lastCommaPos+1);
  unsigned long checkSumGenerated = checkSumFromString(packetWithNoCheckSum);
  if(checkSum == checkSumGenerated){
    return 1;
  }
  return 0;
}

String getPacketDataString(String packet){
  int lastCommaPos = packet.lastIndexOf(",");
  String packetWithNoCheckSum = packet.substring(0,lastCommaPos+1);
  int lastAt = packet.lastIndexOf("@");
  packet = packetWithNoCheckSum.substring(lastAt+1);
  return packet;
}

String getPacketFlag(String packet){
   String flag = "";
   flag = midString(packet,"@","@");
   return flag;
}

byte processIncomingPacket(String packet){
   byte packetHealth = checkPacketHealth(packet);
   if(packetHealth == 1){
      String flag = getPacketFlag(packet);
      String dataString = getPacketDataString(packet);
      flagChecker(flag,dataString);
      return 1;
   }else{
    return 0;
   }
}
String bufferPacketStringForReading = "";
void bufferPacket(String packetDataOnly){
  bufferPacketStringForReading = packetDataOnly;
}

String getFromPack_string(){
  int commaPos = bufferPacketStringForReading.indexOf(",");
  String datum = bufferPacketStringForReading.substring(0,commaPos);
  //update buffer string
  bufferPacketStringForReading = bufferPacketStringForReading.substring(commaPos+1);
  //return datum
  return datum;
}

byte getFromPack_byte(){
  return getFromPack_string().toInt();
}
int getFromPack_int(){
  return getFromPack_string().toInt();
}
long getFromPack_long(){
  return getFromPack_string().toInt();
}
float getFromPack_float(){
  return getFromPack_string().toFloat();
}

///////////////FLAG CHECKER////////////////////////////
// add checks for your flags here and do 
// what you need to with the data
void flagChecker(String flag, String packetDataOnly){
  if(flag == "HALRELAY"){
    bufferPacket(packetDataOnly);
    byte device = getFromPack_byte();
    byte state = getFromPack_byte();
    powerDevice(device,state)
  }

  
}
