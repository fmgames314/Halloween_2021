





byte relayA = 2;
byte relayB = 3;
byte relayC = 4;
byte relayD = 5;
byte mosfetPin = 9;
byte triggerPin = A5;
byte triggerPower = A3;


void setup() 
{
  Serial.begin(9600);
  pinMode(relayA,OUTPUT);
  pinMode(relayB,OUTPUT);
  pinMode(relayC,OUTPUT);
  pinMode(relayD,OUTPUT);
  pinMode(mosfetPin,OUTPUT);
  pinMode(triggerPower,OUTPUT);
  digitalWrite(triggerPower,LOW);
  pinMode(triggerPin,INPUT_PULLUP);
  setRelay(relayA,LOW);
  setRelay(relayB,LOW);
  setRelay(relayC,LOW);
  setRelay(relayD,LOW);
  digitalWrite(mosfetPin,LOW);
  Serial.println("Ready");
  analogWrite(mosfetPin,200);
}

unsigned long mainTimer = 0;
byte canITazer = 1;
void loop() 
{
  int triggerState = !digReadAvg(triggerPin,100);
  if(triggerState == 1 && canITazer == 1){
     //triggered
     canITazer = 0;
     setRelay(relayA,HIGH);//tazer
     setRelay(relayB,HIGH);//box power
     delay(200); // give box time to power on 
     setRelay(relayC,HIGH);//box effect press
     delay(100);
     setRelay(relayC,LOW);//box effect depress

     for(int i = 0; i < 40; i+=1){
      analogWrite(mosfetPin,round(random(100)));
      delay(100);
     }
     
     ///////all off
     setRelay(relayA,LOW);//tazer
     setRelay(relayB,LOW);//box power
     
      analogWrite(mosfetPin,0);
      delay(3000);
      analogWrite(mosfetPin,200);
  }
 

  if(millis()-mainTimer > 12000){
    canITazer = 1;
    mainTimer = millis();
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





void setRelay(byte relayPin, byte state){
  digitalWrite(relayPin,!state);
}


