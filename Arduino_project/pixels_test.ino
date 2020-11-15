/***************************************************************************
  This is a library for the AMG88xx GridEYE 8x8 IR camera

  This sketch tries to read the pixels from the sensor

  Designed specifically to work with the Adafruit AMG88 breakout
  ----> http://www.adafruit.com/products/3538

  These sensors use I2C to communicate. The device's I2C address is 0x69

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Dean Miller for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include <Wire.h>
#include <Adafruit_AMG88xx.h>
#include <stdio.h>
#include <string.h>

Adafruit_AMG88xx amg;

float pixels[AMG88xx_PIXEL_ARRAY_SIZE];
//={'\0'}
//char* loc=pixels_array;

void append(char* s, char c);

void setup() {
    Serial.begin(115200);
    Serial.println(F("AMG88xx pixels"));

    bool status;
    
    // default settings
    status = amg.begin();
    if (!status) {
        Serial.println("Could not find a valid AMG88xx sensor, check wiring!");
        while (1);
    }
    
    Serial.println("-- Pixels Test --");

    Serial.println();

    delay(100); // let sensor boot up
}


void loop() { 
    //read all the pixels
    char pixels_array[512]={'\0'};
    amg.readPixels(pixels);
    //Serial.print("[");
    for(int i=1; i<=AMG88xx_PIXEL_ARRAY_SIZE; i++){
      char aux[32];
      memset(aux,0,sizeof(aux));
      sprintf(aux,"%.2f,", pixels[i-1]);
      //dtostrf(pixels[i-1],6,2,aux);
      strcat(pixels_array,aux);
    }
    //const char aux1[1]={'\n'};
    //strcat(pixels_array,aux1);
    Serial.println(pixels_array);
    //Serial.println(pixels_array);
    //Serial.println("]");
    //Serial.println();

    //delay a second
    delay(100);
}

void append(char* s, char c) {
        int len = strlen(s);
        s[len] = c;
        s[len+1] = '\0';
}
