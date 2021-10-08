






byte dropSwitchDetect = A5; 
byte whiteLED = 10; // outerLED
byte redLED = 9; // innerLED

byte ledA_R = 2;
byte ledA_G = 3;
byte ledA_B = 4;

byte ledB_R = 6;
byte ledB_G = 7;
byte ledB_B = 8;

byte knob = A1;
byte buttonA = A0;
byte buttonB = 12;



void setup() {
  Serial.begin(9600);
  pinMode(ledA_R,OUTPUT);
  pinMode(ledA_G,OUTPUT);
  pinMode(ledA_B,OUTPUT);
  pinMode(ledB_R,OUTPUT);
  pinMode(ledB_G,OUTPUT);
  pinMode(ledB_B,OUTPUT);
  setRGBledA(0,0,0);
  setRGBledB(0,0,0);
  
  pinMode(knob,INPUT_PULLUP);
  pinMode(buttonA,INPUT_PULLUP);
  pinMode(buttonB,INPUT_PULLUP);
  pinMode(dropSwitchDetect,INPUT_PULLUP);
  
  //make sure big led strips are off by default
  pinMode(whiteLED,OUTPUT);
  pinMode(redLED,OUTPUT);
  digitalWrite(whiteLED,LOW);
  digitalWrite(redLED,LOW);
  setRGBledA(1,0,0);delay(100);
  setRGBledA(0,1,0);delay(100);
  setRGBledA(0,0,1);delay(100);
  setRGBledA(1,1,1);delay(1000);
  setRGBledB(1,1,1);delay(1000);
  setRGBledA(0,0,0);
  setRGBledB(0,0,0);
}


byte modeRed = 0;
byte modeWhite = 0;
byte buttonA_value_last = 0;
byte buttonB_value_last = 0;
int redBrightness = 255;
int whiteBrightness = 255;

void loop() {
    byte buttonA_value = !digitalRead(buttonA);
    byte buttonB_value = !digitalRead(buttonB);
    byte knobValue = analogRead(knob);
    byte dropSwitch = !digitalRead(dropSwitchDetect);
    if(buttonA_value == 1 && buttonA_value_last == 0){
      //button A pressed
      modeRed+=1;
      if(modeRed == 4){modeRed = 0;}
    }
    if(buttonB_value == 1 && buttonB_value_last == 0){
      //button B pressed
      modeWhite+=1;
      if(modeWhite == 4){modeWhite = 0;}
    }

//////////////////////////RED LEDD////////////////////////////////
    if(modeRed == 0){
      setRGBledA(1,0,0);
      analogWrite(redLED,LOW);
    }
    if(modeRed == 1){
      setRGBledA(0,0,1);
      if(dropSwitch == 1){
        analogWrite(redLED,redBrightness);
      }
      else{
         analogWrite(redLED,LOW);
      }
    }  
    if(modeRed == 2){
      setRGBledA(0,1,0);
      analogWrite(redLED,redBrightness);
    }  
    if(modeRed == 3){
      setRGBledA(1,1,1);
      analogWrite(redLED,redBrightness);
      redBrightness = map(knobValue,0,1023,0,255);
    }   
/////////WHITE LED////////////////////////////////
 if(modeWhite == 0){
      setRGBledB(1,0,0);
      analogWrite(whiteLED,LOW);
    }
    if(modeWhite == 1){
      setRGBledB(0,0,1);
      if(dropSwitch == 1){
        if(random(20) == 1 )
        {
          analogWrite(whiteLED,whiteBrightness);
          delay(50);
          analogWrite(whiteLED,LOW);
        }
      }
      else{
         analogWrite(whiteLED,LOW);
      }
    }    
    if(modeWhite == 2){ // light up on green switch
      setRGBledB(0,1,0);
      analogWrite(whiteLED,whiteBrightness);
    }
    
    if(modeWhite == 3){
      setRGBledB(1,1,1);
      analogWrite(whiteLED,whiteBrightness);
      whiteBrightness = map(knobValue,0,1023,0,255);
    }   
    ////////////// button resets///////////////////////////
        
    buttonA_value_last = buttonA_value;
    buttonB_value_last = buttonB_value;
    delay(10);
}



void setRGBledA(bool r, bool g, bool b){
  digitalWrite(ledA_R,!r);
  digitalWrite(ledA_G,!g);
  digitalWrite(ledA_B,!b);
}
void setRGBledB(bool r, bool g, bool b){
  digitalWrite(ledB_R,!r);
  digitalWrite(ledB_G,!g);
  digitalWrite(ledB_B,!b);
}




