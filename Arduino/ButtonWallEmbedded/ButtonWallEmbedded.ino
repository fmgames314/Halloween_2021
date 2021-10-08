
byte switchPin = A2;
byte stopLightA = A6;
byte stopLightB = A10;

const int numberOfLeds = 24;
int ledPins[] = {
  43,11,10,9,44,7,6,45,4,3,2,38,39,40,41,42,12,8,5,46,47,48,49,50
  //46,47,48,49,50 are next free ones, 12,8,5 are dead
};
byte ledModes[numberOfLeds];

const int numberOfButts = 16;
int buttPins[] = {
  22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37
};
byte buttonLastState[numberOfButts];

void setup() {
  Serial.begin(9600);
  for(int i = 0; i < numberOfLeds; i+=1){
    pinMode(ledPins[i],OUTPUT);
    digitalWrite(ledPins[i],HIGH);
    delay(200);
  }
   for(int i = 0; i < numberOfLeds; i+=1){
    digitalWrite(ledPins[i],LOW);
    delay(20);
  }  

    
  for(int i = 0; i < numberOfButts; i+=1){
    pinMode(buttPins[i],INPUT_PULLUP);
  }

  pinMode(switchPin,INPUT_PULLUP);
  pinMode(stopLightA,OUTPUT);
  pinMode(stopLightB,OUTPUT);
  digitalWrite(stopLightA,HIGH);
  digitalWrite(stopLightB,LOW);
}

void loop() {
  ledControl();
  checkSerial(Serial);
  
  for(int i = 0; i < numberOfButts; i+=1){
    byte butState = !digReadAvg(buttPins[i],100);
    if(butState > buttonLastState[i]){ // button Pressed
      Serial.println("P,"+String(i));
    }
    if(butState < buttonLastState[i]){ // button depressed
      Serial.println("R,"+String(i));
    }
    buttonLastState[i] = butState;
  } // button check and serial end

  /////check for stoplight switch//////
  if(digitalRead(switchPin) == HIGH ){
    digitalWrite(stopLightA,HIGH);
    digitalWrite(stopLightB,LOW);
  }
  else{
    digitalWrite(stopLightA,LOW);
    digitalWrite(stopLightB,HIGH);
  }

}

void ledControl(){
    for(int i = 0; i < numberOfLeds; i+=1){
      int mode = ledModes[i];
      if(mode == 0){digitalWrite(ledPins[i],LOW);}
      if(mode == 1){digitalWrite(ledPins[i],HIGH);}
      if(mode == 2){
        digitalWrite(ledPins[i],HIGH); // fade?
      }
    }
}




bool digReadAvg(int pin,int numOfReads){
  int numOfHigh = 0;  
  int numOfLow = 0;  
  for(int i = 0; i < numOfReads; i+=1){
    int stateRead = digitalRead(pin);
    if (stateRead == 0){numOfLow+=1;}
    if (stateRead == 1){numOfHigh+=1;}
  }
  if(numOfHigh > numOfLow){return HIGH;}
  if(numOfLow > numOfHigh){return LOW;}
}






       
void checkFlags(HardwareSerial &refSer, String FlagFound)
{
      if(FlagFound == "@LED") 
      {
         int ledNum = SerialReadInt(refSer);
         int ledstate = SerialReadInt(refSer);
         ledModes[ledNum] = ledstate;
      }  
}
void checkSerial(HardwareSerial &refSer)
{
  while (refSer.available())
  {
    String FlagFound = "";
    char tmpBit = refSer.read();
    if(char(tmpBit) == '@')
    {
      FlagFound+=tmpBit;
      SerialWaitforData(refSer);  FlagFound+=char(refSer.read());
      SerialWaitforData(refSer);  FlagFound+=char(refSer.read());
      SerialWaitforData(refSer);  FlagFound+=char(refSer.read());
      checkFlags(refSer,FlagFound);
    }   
    
  
  } // end serial 3 available

}



void SerialWaitforData(HardwareSerial &refSer)
{
unsigned long Whilecountend = millis();  
while(refSer.available() == 0)
{if(millis()-Whilecountend > 500) {break;}  }
}


int SerialReadInt(HardwareSerial &refSer)
{
  int markOfQuestions = 0;
  String TmpData = "";
  unsigned long Whilecountend = millis(); 
   while(markOfQuestions == 0)
   {
   SerialWaitforData(refSer);
    char b1 = refSer.read();
    if(char(b1) == '?')
    {
      return (TmpData.toInt()); 
      markOfQuestions = 1;
      break;
    }
    
    if(byte(b1) != 255) 
    {
    //  Serial.println("Added char: "+String(b1)+" Which is :"+byte(b1));
      TmpData+=String(b1);
      }
    if(millis()-Whilecountend > 50) {break;}
    }// end while loop

}


String SerialReadString(HardwareSerial &refSer)
{
  int markOfQuestions = 0;
  String TmpData = "";
  unsigned long Whilecountend = millis(); 
   while(markOfQuestions == 0)
   {
    SerialWaitforData(refSer);
    char b1 = refSer.read();
    if(char(b1) == '?')
    {
      return (TmpData); 
      markOfQuestions = 1;
      break;
    }
    
    if(byte(b1) != 255) 
    {
    //  Serial.println("Added char: "+String(b1)+" Which is :"+byte(b1));
      TmpData+=String(b1);
      }
    if(millis()-Whilecountend > 50) {break;}
    }// end while loop
     
}// end xbee float

