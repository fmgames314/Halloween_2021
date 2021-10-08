#include <Servo.h>
Servo airMotor;
#define MAX_SIGNAL 2000
#define NETRUAL 1400
#define MIN_SIGNAL 1100
#define MOTOR_PIN 9 

void setup() 
{
  delay(7000);
  Serial.begin(9600);
  airMotor.attach(MOTOR_PIN); // all this crap is for brushless motor controller
  Serial.println("Setting up motor");
  delay(100);
  setFanPower(50);
  delay(100);
  setFanPower(100);
  delay(100);
  setFanPower(0);
  delay(300);
  setFanPower(50);
  delay(3000);
  setFanPower(60);
  delay(3000);
  setFanPower(50);
  Serial.println("Finished with power config");
  delay(1000);
  Serial.println("Starting Loop");
}



void loop() 
{
  Serial.println("ON");
  setFanPower(100);
  delay(2000);
  setFanPower(50);
  Serial.println("OFF");
  delay(5000);

}





void setFanPower(byte percent)
{
    if(percent > 0){airMotor.attach(MOTOR_PIN);} // attach if power is needed
    int value = map(percent,0,100,MIN_SIGNAL,MAX_SIGNAL);
    airMotor.writeMicroseconds(value);  
    
}

