


byte eyeballPower = 8;
byte eyeballTrigger = 9;
byte lanternA = 10;
byte lanternB = 11;
byte triggerA = A0;
byte triggerB = A1;


void setup() {
  Serial.begin(9600);
  pinMode(eyeballPower,OUTPUT);
  pinMode(eyeballTrigger,OUTPUT);
  pinMode(lanternA,OUTPUT);
  pinMode(lanternB,OUTPUT);
  pinMode(triggerA,INPUT_PULLUP);
  pinMode(triggerB,INPUT_PULLUP);
  digitalWrite(lanternA,LOW); 
  digitalWrite(lanternB,LOW); 

}

byte eyeBallStage = 0;
byte lanternStage = 0;
unsigned long lanternTimer = 0;

void loop() {
  //trigger pins
  byte trigStateA = !digitalRead(triggerA);
  byte trigStateB = !digitalRead(triggerB);
  

  if(trigStateB == 1 && lanternStage == 0){
    lanternStage = 1;
    lanternTimer = millis();
    digitalWrite(lanternA,HIGH); // lantern A On
  }
  if(lanternStage == 1 && millis()-lanternTimer > 800){
    lanternStage = 2;
    digitalWrite(lanternB,HIGH); // lantern B On
  }

   if(trigStateB == 0 && lanternStage == 2){
    lanternStage = 0;
    digitalWrite(lanternA,LOW); 
    digitalWrite(lanternB,LOW); 
  }


  
  //////eyeball
  if(trigStateA == 1 && eyeBallStage == 0){
    eyeBallStage = 1;
  }
  if(trigStateA == 0 && eyeBallStage == 2){ // turn off
    digitalWrite(eyeballTrigger,HIGH);
    delay(100);
    digitalWrite(eyeballTrigger,LOW);
    delay(800);
    digitalWrite(eyeballPower,LOW);
    eyeBallStage = 0;
  }
  
  if(eyeBallStage == 1){
    digitalWrite(eyeballPower,HIGH);
    delay(100);
    digitalWrite(eyeballTrigger,HIGH);
    delay(100);
    digitalWrite(eyeballTrigger,LOW);
    eyeBallStage = 2;
  }
  

}










