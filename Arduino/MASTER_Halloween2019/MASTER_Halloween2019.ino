

byte ACrelay_1 = 9;
byte ACrelay_2 = 10;
byte ACrelay_3 = 11;
byte ACrelay_4 = 12;


byte relay_1 = 22;
byte relay_2 = 24;
byte relay_3 = 26;
byte relay_4 = 28;
byte relay_5 = 30;
byte relay_6 = 32;
byte relay_7 = 34;
byte relay_8 = 36;
byte relay_9 = 2;
byte relay_10 = 3;
byte relay_11 = 4;
byte relay_12 = 5;
byte relay_13 = 6;
byte relay_14 = 38;
byte relay_15 = 7;
byte relay_16 = 8;

byte listOfOutputs[]={ACrelay_1,ACrelay_2,ACrelay_3,ACrelay_4,relay_1,relay_2,relay_3,relay_4,relay_5,relay_6,relay_7,relay_8,relay_9,relay_10,relay_11,relay_12,relay_13,relay_14,relay_15,relay_16};
byte numOfThing = 20;

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  for(int i = 0; i < numOfThing; i+=1){
    pinMode(listOfOutputs[i],OUTPUT);
    digitalWrite(listOfOutputs[i],HIGH); 
  }

}

void loop() {
    String incomingPacket = Serial2.readStringUntil('\n'); 
    byte packetStatus = processIncomingPacket(incomingPacket);
    // use packetStatus to check if packet had good or bad checksum
    if(packetStatus == 1){
      Serial.println("Good Checksum");
    }
    else{
      Serial.println("BAD Checksum!");
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
    digitalWrite(listOfOutputs[device],state); 
  }
  if(flag == "RFRELAY"){
    bufferPacket(packetDataOnly);
    String outlet = getFromPack_string();
    String bitrate = getFromPack_string();
    String pulse = getFromPack_string();
    Serial3.print("@PDS"+outlet+"?"+bitrate+"?"+pulse+"?");
  }
  
}
