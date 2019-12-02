/*
  ButtonMouseControl

  For Leonardo and Due boards only.

  Controls the mouse from five pushbuttons on an Arduino Leonardo, Micro or Due.

  Hardware:
  - five pushbuttons attached to D2, D3, D4, D5, D6

  The mouse movement is always relative. This sketch reads four pushbuttons,
  and uses them to set the movement of the mouse.

  WARNING: When you use the Mouse.move() command, the Arduino takes over your
  mouse! Make sure you have control before you use the mouse commands.

  created 15 Mar 2012
  modified 27 Mar 2012
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/ButtonMouseControl
*/

#include "Mouse.h"

const int analogInPin = A5;  // Analog input pin that the potentiometer is attached to

// set pin numbers for the five buttons:
const int upButton = 2;
const int downButton = 3;
const int leftButton = 4;
const int rightButton = 5;
const int mouseButton = 6;

int range = 5;              // output range of X or Y movement; affects movement speed
int responseDelay = 10;     // response delay of the mouse, in ms

int circonference = 20;
int circonferenceBack = -20;
int delayInnerMoveMultiplier =2;

void setup() {
  delay(1200);
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  delay(100);
  Serial.print("Starting... ");
  delay(2800);
  pinMode(13,OUTPUT);
  
  // initialize the buttons' inputs:
  pinMode(upButton, INPUT);
  pinMode(downButton, INPUT);
  pinMode(leftButton, INPUT);
  pinMode(rightButton, INPUT);
  pinMode(mouseButton, INPUT);
  // initialize mouse control:
  Mouse.begin();
  Serial.print("Started ");
}
int flag = 0;

int circling = 3000;
void loop() {
 //digitalWrite(13,HIGH);
 delay(500);

 // Serial.print(".");
  flag = analogRead(A4);
 // Serial.print(flag);
  
 if (flag> 400)
 {
  
  Serial.print(":\n");
  //login when pin 3 is HIGH, we want to Focus render on where the mouse is
  //First iteration will just hold pressed the button and move the mouse around 20-50 pixel in circle
   digitalWrite(13,HIGH);

   int x = circonference;
   int y = circonference;
   
   mover(x,y);
   
    x = 0;
    y = circonferenceBack;
    
   mover(x,y);
   
    x = circonferenceBack;
    y = 0;
    
   mover(x,y);

    x = circonferenceBack;
    y = circonferenceBack;
    
   mover(x,y);



   digitalWrite(13,LOW);

  // a delay so the mouse doesn't move too fast:
  delay(responseDelay);
  
     digitalWrite(13,LOW);
 }

  delay(responseDelay);
}

int mover(int x,int y)
{
  
     flag = analogRead(A4);
    if (flag> 400) { 
     Mouse.move(x, y, 0);
      
      Mouse.press(MOUSE_RIGHT);
     delay(circling * delayInnerMoveMultiplier);
      Mouse.release(MOUSE_RIGHT);
    }

}
