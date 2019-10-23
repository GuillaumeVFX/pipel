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

int circonference = 40;
int circonferenceBack = -40;

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
bool f = true;
int circling = 3000;
void loop() {
 digitalWrite(13,HIGH);
 delay(500);
  if (f)
  {
    Serial.print(".");
    int flag = analogRead(A4);
    Serial.print(flag);
    
   if (flag> 400)
   {
    
    Serial.print(":\n");
    //login when pin 3 is HIGH, we want to Focus render on where the mouse is
    //First iteration will just hold pressed the button and move the mouse around 20-50 pixel in circle
     digitalWrite(13,HIGH);
     
     flag = analogRead(A4);
    if (flag> 400) { 
     Mouse.move(circonference, circonference, 0);
      if (!Mouse.isPressed(MOUSE_LEFT)) {
      Mouse.press(MOUSE_LEFT);
     delay(circling);
      Mouse.release(MOUSE_LEFT);
    }

     flag = analogRead(A4);
     if (flag> 400) { Mouse.move(0, circonferenceBack, 0);
      if (!Mouse.isPressed(MOUSE_LEFT)) {
      Mouse.press(MOUSE_LEFT);
     delay(circling);
      Mouse.release(MOUSE_LEFT);
     }

     flag = analogRead(A4);
    if (flag> 400) {  Mouse.move(circonferenceBack, 0, 0); if (!Mouse.isPressed(MOUSE_LEFT)) {
      Mouse.press(MOUSE_LEFT);
     delay(circling);
      Mouse.release(MOUSE_LEFT);
    }
    else{
        
     
      
      }


     digitalWrite(13,LOW);
   }
  } 
  else { //stuff of the sample
    
  
  // read the buttons:
  int upState = digitalRead(upButton);
  int downState = digitalRead(downButton);
  int rightState = digitalRead(rightButton);
  int leftState = digitalRead(leftButton);
  int clickState = digitalRead(mouseButton);

  // calculate the movement distance based on the button states:
  int  xDistance = (leftState - rightState) * range;
  int  yDistance = (upState - downState) * range;

  // if X or Y is non-zero, move:
  if ((xDistance != 0) || (yDistance != 0)) {
    Mouse.move(xDistance, yDistance, 0);
  }

  // if the mouse button is pressed:
  if (clickState == HIGH) {
    // if the mouse is not pressed, press it:
    if (!Mouse.isPressed(MOUSE_LEFT)) {
      Mouse.press(MOUSE_LEFT);
    }
  }
  // else the mouse button is not pressed:
  else {
    // if the mouse is pressed, release it:
    if (Mouse.isPressed(MOUSE_LEFT)) {
      Mouse.release(MOUSE_LEFT);
    }
  }

    }
  // a delay so the mouse doesn't move too fast:
  delay(responseDelay);
  
     digitalWrite(13,LOW);
  delay(responseDelay);
}
