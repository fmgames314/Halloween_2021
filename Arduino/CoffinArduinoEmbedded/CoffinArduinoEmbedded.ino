#include <SoftwareSerial.h>
SoftwareSerial mp3Trigger(2, 3); // RX, TX


byte lidSwitch = 7;
byte footPedalA = A0;
byte footPedalB = A1;
byte footPedalC = A2;

byte relayA = 8;
byte relayB = 9;
byte relayC = 10;
byte relayD = 11;


void setup() {
  //mp3 serial port
  Serial.begin(9600); //Serial for MP3 Board
  mp3Trigger.begin(38400);
  //pine modes
  pinMode(lidSwitch, INPUT_PULLUP);
  pinMode(relayA, OUTPUT);
  pinMode(relayB, OUTPUT);
  pinMode(relayC, OUTPUT);
  pinMode(relayD, OUTPUT);
  digitalWrite(relayA,HIGH);
  digitalWrite(relayB,HIGH);
  digitalWrite(relayC,HIGH);
  digitalWrite(relayD,HIGH);

  pinMode(footPedalA, INPUT_PULLUP);
  pinMode(footPedalB, INPUT_PULLUP);
  pinMode(footPedalC, INPUT_PULLUP);
  mp3Trigger.write('T'); mp3Trigger.write("6");
  Serial.println("Ready");
}

byte FP_A_Last = 0;
byte FP_B_Last = 0;
byte FP_C_Last = 0;
byte lidSwitchLast = 0;
byte shiftState = 0;
byte coffinState = 0;

void loop() {
  //coffin background
  coffinBackground();
  /////////////////read switches/////////////////////
  byte FP_A_State = !digitalRead(footPedalA);
  byte FP_B_State = !digitalRead(footPedalB);
  byte FP_C_State = !digitalRead(footPedalC);
  byte lidSwitchState = !digitalRead(lidSwitch);
  ///print for debug////
  if (FP_A_State == 1 && FP_A_Last == 0) {Serial.println("Shift Pedal A Pressed");}
  if (FP_B_State == 1 && FP_B_Last == 0) {Serial.println("fog/bumper Pedal B Pressed");}
  if (FP_C_State == 1 && FP_C_Last == 0) {Serial.println("sound/coffin Pedal C Pressed");}
  
  //map shift state with pedal A
  shiftState = FP_A_State;
  // if shift is not pressed
  if (shiftState == 0) {
    if (FP_B_State == 1) {
      digitalWrite(relayA, LOW);
    } else {
      digitalWrite(relayA, HIGH);
    }
    if (FP_C_State == 1 && FP_C_Last == 0) {
       //pedal C is pressed, play bang sound
       mp3Trigger.write('T'); mp3Trigger.write("5");
       Serial.println("playing spooky sound");
    }
  }else{
    //shift pedal is pressed
    if (FP_B_State == 1 && FP_B_Last == 0) {
        if(getCoffinPos() == 0){
          digitalWrite(relayD, LOW);
          delay(300);
          digitalWrite(relayD, HIGH);
        }
    }
    if (FP_C_State == 1 && FP_C_Last == 0) {
        coffinState = !coffinState;  
        byte sucess = setCoffin(coffinState);  
        if(sucess == 0){coffinState = !coffinState;}
    }

    
  }

  //check pedal B
  if (FP_B_State == 1 && FP_B_Last == 0) {
    //pedal b is pressed
  }


  //remember last state of switches
  FP_A_Last = FP_A_State;
  FP_B_Last = FP_B_State;
  FP_C_Last = FP_C_State;
  delay(10);
}



byte cofMoving = 0;
byte coffinPosition = 0;
byte cofStage = 0;
void coffinBackground(){
  if(coffinPosition == 0 && cofMoving == 1){
    // want to open and coffin is in closed position
    if(cofStage == 0){
      digitalWrite(relayD, LOW);
      cofStage = 1;
    }
    if(cofStage == 1){
      byte lidSwitchState = !digitalRead(lidSwitch);
      if(lidSwitchState == 1){ // lid is fully open, deploy skeleton
        digitalWrite(relayC, LOW);
        mp3Trigger.write('T'); mp3Trigger.write("3"); // bump sound effect
        delay(1000);
        mp3Trigger.write('T'); mp3Trigger.write("8"); // bump sound effect
        cofStage = 2;
        coffinPosition = 1; // coffin is now open
        cofMoving = 0; // coffin is done moving
      }
    }
  } // coffin open code.
//////////////////////////
  if(coffinPosition == 1 && cofMoving == 1){
    // want to close and coffin is in open position
    if(cofStage == 0){
      digitalWrite(relayC, HIGH); // lower the skeleton
      delay(2000);
      digitalWrite(relayD, HIGH); // CLOSE THE LID
      cofStage = 1;
      delay(200);
    }
    if(cofStage == 1){
      byte lidSwitchState = !digitalRead(lidSwitch);
      if(lidSwitchState == 0){ // lid is shut now
        cofStage = 2;
        coffinPosition = 0; // coffin is now close
        cofMoving = 0; // coffin is done moving
      }
    }
  } // coffin open code.  
} // coffin background end function



byte setCoffin(byte IwantToGoTo){
  if(cofMoving == 1){
    return 0;
  }else{
    if(IwantToGoTo == 1){ /// I want the coffin to open
      if(coffinPosition == 0){ // if coffin is completely closed
        cofMoving = 1;
        cofStage = 0;
        return 1;
        // open up
      }
    }
    if(IwantToGoTo == 0){ // I want the coffin to close now
      if(coffinPosition == 1){ // only if it's fully open 
        cofMoving = 1;
        cofStage = 0;
        return 1;
        // close
      }
    }
  }

  return 0;
}


byte getCoffinPos(){
  return coffinPosition+cofMoving;
}



