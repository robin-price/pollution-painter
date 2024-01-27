# Pollution Painter (pi 0 build)

## Overview
The Pollution Painter is a digital light painter that allows you to visualise particulate pollution levels through long exposure photography. LEDs responding to the pollution levels draw particles of light to represent particles of pollution. The effect is as if the air has been put under a microscope and lit up allowing the invisible particulates to be seen.

I built my first pollution painter in 2017 and have rebuilt, fixed and adapted it multiple times over the last seven years taking photographs of pollution levels around the world. You can [read more about the original Air of the Anthropocene project here.](https://stuffwhatidid.com/air-of-the-anthropocene)

In the interests of cutting my own pollution emissions I am now open sourcing the design and instructions in the hope that you might take these photos and collaborate with me to draw attention to pollution in your environment. Please send any photos with details of date, location and observed PM2.5 levels to robin@robinprice.net

## Design notes
The original pollution painter was built out of scraps from other projects I had lying around my studio. It used to use a single raspberry pi 0, e-ink display and WS2811 neopixel LEDs but after the delicate e-I'll displays kept breaking I moved to using the pi 0 as a WiFi access point and reading the PM2.5 data and adjusting settings with my mobile phone. The arduino got soldered into the design after an update to raspbian made the LED timings wonky and unreliable resulting in streaky photos. Off loading the code for the lights exclusively to the Arduino made things much better and makes sense given raspbian’s non real time status. Also back when I started the project I was kindly loaned an Alphasense OPC-N2 by my long time collaborator Prof. Francis Pope. This open source design uses the cheaper and widely available nova SDS011. 

I have been working on a new design built around a single raspberry pi pico and simple custom PCB that streamlines the design but this pi 0 version is presented here because you might have some of these items lying around your studio / workshop / classroom. It’s also perhaps easer to adapt or develop than the pico as you’ve a full raspbian stack with python and all its libraries as well as an Arduino to play with.

All of the designs, my original, this open source pi 0 one and the pico share the same way of working. The wrist worn sensor detects particulate PM2.5 pollution and reports this electronically to the pi. The pi records, interpolates and temporally smoothes the data a little and maps it to a value between 0 and 255. This is sent to the Arduino which uses it when visualising the data during a long exposure photograph. The Arduino very quickly loops through all the LEDS connected and randomly decides whether to turn each one briefly on based the 0 - 255 value sent from the pi. The more particles of pollution the sensor detects the higher the probability of the LEDs twinkling hence the higher particles of light in the final photograph. The calibration curve was designed for aesthetic effect and based on the readings I experienced in Delhi being the highest upper limit on the mapping scale. A trigger button wired to the pi fades the LEDs in and out during photography. I usually use a microphone boom pole to hold the LEDs up while I walk in front of the camera but this design uses a cheaper fishing rod, I invite you to find your own creative solution…

The whole device is powered from a USB battery pack with two 2.4A USB A outlets, one for the pi, sensor and Arduino the other exclusively for the LEDs. The circuits share a common ground and the design is very much influenced by Adafruit’s digital light painter, but also Steve Mann and Timo Arnall.

For my original device I used three roughly two metre long strips of WS2811 30 LED per metre LED tape. These were gaffa taped together at roughly 1 cm offsets to create the illusion of a single roll of a more expensive LED tape with more LEDS. I had a ton of LED tape left lying round the studio after a previous project. This design tries to cut costs and bring it up to date with two one metre strips of 60 LED per metre Dotstar (APA 102) LEDs. I recommend taping these together so the LEDs on one strip line up with the spaces on the other to create the effect of more LEDs. I recommend getting weatherproof LEDs as sometimes it rains outdoors where you take photographs and the plastic covering doubles as a nifty light diffuser.

##BOM

| Item | Description | UK Supplier Link|
|---|---|---|
Pi zero w | Raspberry Pi MCU | https://shop.pimoroni.com/products/raspberry-pi-zero-w?variant=39458414264403 
| 
Circuit Diagam 

1. Prepare pi by soldering header strip
2. Solder Arduino and level shifter (or just header strip and tape depending how confident you feel)
3. Solder all jumper wires on perma proto board
4. Solder connector to LED strip
5. Make LED data and power cables
6. Solder button
7. Flash Arduino
8. Flash pi sd
9. Test
