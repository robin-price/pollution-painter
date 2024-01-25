#include <FastLED.h>

#define NUM_LEDS 240
#define DATA_PIN    11
#define CLOCK_PIN   13

// Define the array of leds
CRGB leds[NUM_LEDS];

unsigned int cutoff = 250;
unsigned int brightness = 20;
unsigned int wait = 10;
unsigned int fade = 5000;
unsigned int currentBrightness;
int state = 0;

unsigned long lastUpdate;
unsigned long startTime;

const byte numChars = 32;
char receivedChars[numChars];
bool newData = false;

void setup() {
  FastLED.addLeds<DOTSTAR, DATA_PIN, CLOCK_PIN, BGR>(leds, NUM_LEDS); 
  Serial.begin(9600);
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}


void loop() {
  recvWithStartEndMarkers();
  if (newData) {
    //Serial.println(receivedChars);
    String inputString(receivedChars);
    Serial.print(inputString);
    if (inputString.startsWith("cutoff ") && inputString.length() == 10) {
      cutoff = constrain(inputString.substring(7).toInt(),0, 255);
//      Serial.print("cutoff ");
//      Serial.println(cutoff, DEC);
    } else if (inputString.startsWith("brightness ") && inputString.length() == 14) {
      brightness = constrain(inputString.substring(11).toInt(), 0, 255);
      FastLED.setBrightness(brightness);
//      Serial.print("brightness ");
//      Serial.println(brightness, DEC);
    } else if (inputString.startsWith("wait ") && inputString.length() == 8) {
      wait = inputString.substring(5).toInt();
//      Serial.print("wait ");
//      Serial.println(wait, DEC);
    } else if (inputString.startsWith("fade ") && inputString.length() == 9) {
      fade = inputString.substring(5).toInt();
//      Serial.print("fade ");
//      Serial.println(fade, DEC);
    } else if (inputString.startsWith("start")) {
      state = 1;
      startTime = millis();
//      Serial.println("starting");
    } else if (inputString.startsWith("stop")) {
      state = 3;
      startTime = millis();
//      Serial.println("stopping");
    }
    newData = false;
  }

  if (millis() - lastUpdate > wait) {
    switch (state) {
      case 0:
        for (int i = 0; i < NUM_LEDS; i++) {
          leds[i] = CRGB::Black;
        }
        break;
      case 1:
        if (millis() - startTime < fade) {
          for (int i = 0; i < NUM_LEDS; i++) {
            if (cutoff < random(256)) {
              leds[i] = CRGB::White;
            } else {
              leds[i] = CRGB::Black;
            }
          }
          currentBrightness = map(millis() - startTime, 0, fade, 0, brightness);
          FastLED.setBrightness(currentBrightness);
        } else {
          for (int i = 0; i < NUM_LEDS; i++) {
            if (cutoff < random(256)) {
              leds[i] = CRGB::White;
            } else {
              leds[i] = CRGB::Black;
            }
          }
          currentBrightness = brightness;
          FastLED.setBrightness(currentBrightness);
          state = 2;
        }
        break;
      case 2:
        for (int i = 0; i < NUM_LEDS; i++) {
          if (cutoff < random(256)) {
            leds[i] = CRGB::White;
          } else {
            leds[i] = CRGB::Black;
          }
        }
        break;
      case 3:
        if (millis() - startTime < fade) {
          for (int i = 0; i < NUM_LEDS; i++) {
            if (cutoff < random(256)) {
              leds[i] = CRGB::White;
            } else {
              leds[i] = CRGB::Black;
            }
          }
          currentBrightness = map(millis() - startTime, 0, fade, currentBrightness, 0);
          FastLED.setBrightness(currentBrightness);
          //strip.setBrightness(map(millis() - startTime, 0, fade, currentBrightness, 0));
        } else {
          for (int i = 0; i < NUM_LEDS; i++) {
            leds[i] = CRGB::Black;
          }
          FastLED.setBrightness(0);
          state = 0;
        }
        break;
    }
    FastLED.show();
    lastUpdate = millis();
  }
}
