// 1 indicates pi1 is in control
// 0 indicates pi0 is in control
unsigned int controller = 0;
// pi0 voltage reading
unsigned int pi0Reading = 0;
// pi1 voltage reading
unsigned int pi1Reading = 0;
// number of seconds passed by
unsigned  Time;
// number of seconds to before toggling pi's control to the led
unsigned long TIME_INTERVAL = 10;
// comparison number for checking if TIME_INTERVAL seconds has passed
unsigned long deadtime;

void setup() 
{
  pinMode(6, INPUT);          // pi0 voltage detector
  pinMode(7, INPUT);          // pi1voltage detector
  pinMode(12, OUTPUT);         // LED controller
  pinMode(13, OUTPUT);        // on-board led   
  TAKE OUT FOR FINAL PRODUCTION CODE
  Time = millis();          // current time
  Serial.begin(9600);
  
}

void loop() 
{
  Time = millis();    // get current time
  // check if TIME_INTERVAL seconds has passed by
  if ( (Time > deadtime ) )
  {

    // toggles the controller variable
    controller = 1 - controller;

    // indicate who controls the LED for debugging
    TAKE OUT LATER FOR FINAL PRODUCTION CODE
      if (controller == 1) {
      digitalWrite(13, HIGH);
    } else {
      digitalWrite(13, LOW);
    }
    // reset the deadtime
    deadtime = millis() + (TIME_INTERVAL*1000);

  }
  else 
  {
    // read pi0 and pi1 voltage levels
    pi0Reading = digitalRead(6);
    pi1Reading = digitalRead(7);
    Serial.print(" pi0: "); Serial.println(pi0Reading);
    Serial.print("pi 1 --> ");Serial.println(pi0Reading);

    // conditions for pin 6 and state = 0 (pi 0)
    if ((pi0Reading == HIGH) && (controller == 0)) 
    {
      //digitalWrite(13, HIGH);
      digitalWrite(12, HIGH);
      Serial.println("success");
    } 
    else 
    {
      //digitalWrite(13, LOW);
      digitalWrite(12, LOW);
      Serial.println("failure");
    }
    // conditions for pin 7 and state = 1
    if ((pi1Reading == HIGH) && (controller == 1)) 
    {
      //digitalWrite(13, HIGH);
      digitalWrite(12, HIGH);
    }    
    else 
    {
    //digitalWrite(13, LOW);
    digitalWrite(12, LOW);
    }
  }

}
