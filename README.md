# Pollution Painter (pi 0 build)

## Overview
The Pollution Painter is a digital light painter that allows you to visualise particulate pollution levels through long exposure photography. LEDs responding to the pollution levels draw particles of light to represent particles of pollution. The effect is as if the air has been put under a microscope and lit up allowing the invisible particulates to be seen.

I built my first pollution painter in 2017 and have rebuilt, fixed and adapted it multiple times over the last seven years taking photographs of pollution levels around the world. You can [read more about the original Air of the Anthropocene project here.](https://stuffwhatidid.com/air-of-the-anthropocene)

In the interests of cutting my own pollution emissions I am now open sourcing the design and instructions in the hope that you might take these photos and collaborate with me to draw attention to pollution in your environment. Please send any photos with details of date, location and observed PM2.5 levels to robin@robinprice.net

## Design notes
The original pollution painter was built out of scraps from other projects I had lying around my studio. It used to use a single raspberry pi 0, e-ink display and WS2811 neopixel LEDs but after the delicate e-I'll displays kept breaking I moved to using the pi 0 as a WiFi access point and reading the PM2.5 data and adjusting settings with my mobile phone. The arduino got soldered into the design after an update to raspbian made the LED timings wonky and unreliable resulting in streaky photos. Off loading the code for the lights exclusively to the Arduino made things much better and makes sense given raspbian’s non real time status. Also back when I started the project I was kindly loaned an Alphasense OPC-N2 by my long time collaborator Prof. Francis Pope. This open source design uses the cheaper and widely available nova SDS011. 

I have been working on a new design built around a single raspberry pi pico and simple custom PCB that streamlines the design but this pi 0 version is presented here because you might have some of these items lying around your studio / workshop / classroom. It’s also perhaps easer to adapt or develop than the pico as you’ve a full raspbian stack with python and all its libraries as well as an Arduino to play with.

All of the designs, my original, this open source pi 0 one and the pico share the same way of working. The wrist worn sensor detects particulate PM2.5 pollution and reports this electronically to the pi. The pi records, interpolates and temporally smoothes the data a little and maps it to a value between 0 and 255. This is sent to the Arduino which uses it when visualising the data during a long exposure photograph. The Arduino very quickly loops through all the LEDS connected and randomly decides whether to turn each one briefly on based the 0 - 255 value sent from the pi. The more particles of pollution the sensor detects the higher the probability of the LEDs twinkling hence the higher particles of light in the final photograph. The calibration curve was designed for aesthetic effect and based on the readings I experienced in Delhi being the highest upper limit on the mapping scale. A trigger button wired to the pi fades the LEDs in and out during photography. I usually use a microphone boom pole to hold the LEDs up while I walk in front of the camera but this design uses a cheaper fishing rod, I invite you to find your own creative solution…

The whole device is powered from a USB battery pack with two 2.4A USB A outlets, one for the pi, sensor and Arduino the other exclusively for the LEDs. The circuits share a common ground and the design is very much influenced by [Adafruit’s digital light painter](https://learn.adafruit.com/dotstar-pi-painter/overview), but also [Steve Mann](https://en.wikipedia.org/wiki/Steve_Mann_(inventor)) and [Timo Arnall](https://www.elasticspace.com/2013/09/the-immaterials-project).

For my original device I used three roughly two metre long strips of WS2811 30 LED per metre LED tape. These were gaffa taped together at roughly 1 cm offsets to create the illusion of a single roll of a more expensive LED tape with more LEDS. I had a ton of LED tape left lying round the studio after a previous project. This design tries to cut costs and bring it up to date with two one metre strips of 60 LED per metre Dotstar (APA 102) LEDs. I recommend taping these together so the LEDs on one strip line up with the spaces on the other to create the effect of more LEDs. I recommend getting weatherproof LEDs as sometimes it rains outdoors where you take photographs and the plastic covering doubles as a nifty light diffuser.

## BOM

| Item | Description | UK Supplier Link|
|---|---|---|
| Extensible fishing pole | I use this to fix the LED strip to sometimes with elastic bands, sometimes with bits of insulation tape | [Amazon](https://www.amazon.co.uk/dp/B017NQZZ2Q?psc=1&ref=ppx_yo2ov_dt_b_product_details) |
Pi zero W | Raspberry Pi MCU,  get one with the header socket | [Pimoroni](https://shop.pimoroni.com/products/raspberry-pi-zero-w?variant=39458414264403) |
| Dotstar LED tape | 2m strip of 60 LED / m tape doubled back on itself to make a 1m strip of 120 LED / m | [Cool Components](https://coolcomponents.co.uk/products/apa102-digital-white-addressable-led-weatherproof-strip-60-led-4m?_pos=3&_sid=9ca8ac2bc&_ss=r) |
| SDS011 | Nova PM 2.5 particulate sensor | [Amazon](https://www.amazon.co.uk/DollaTek-Precision-Quality-Detection-Sensors/dp/B07M6JWCWQ/ref=sr_1_7?crid=22VF69APUO84J&keywords=sds011+sensor&qid=1684939626&sprefix=sds0%2Caps%2C137&sr=8-7) |
| USB Battery Charger | You need a model with two 2.4A USB A outlets | [Argos](https://www.argos.co.uk/product/9215346?clickSR=slp:term:portable%20powerbank:3:65:1) |
| 18 AWG Wire | Thicker wire used for supplying current for the LEDs, doubles up for the trigger button too | [Amazon](https://www.amazon.co.uk/dp/B08F7TS37H/ref=redir_mobile_desktop?_encoding=UTF8&aaxitk=76f6fa4d49e304c2faa58fe7688cfb49&content-id=amzn1.sym.5e63d04b-217e-48e0-b230-d463f07fd1e0%3Aamzn1.sym.5e63d04b-217e-48e0-b230-d463f07fd1e0&hsa_cr_id=9199782550402&pd_rd_plhdr=t&pd_rd_r=6cc08f30-8e42-4e47-82af-ac862e4f6c99&pd_rd_w=ckptd&pd_rd_wg=JEEPl&qid=1684939845&ref_=sbx_be_s_sparkle_mcd_asin_0_title&sr=1-1-e0fa1fdd-d857-4087-adda-5bd576b25987) |
| 26 AWG Instrument Wire | I use this to wire up the chips on the protoboard, you can use whatever wire you have handy | [Amazon] (https://www.amazon.co.uk/Stranded-Electrical-Flexible-Silicone-Electric/dp/B09Y99PMRM/ref=sr_1_24?crid=1PY5P4R8QT3O9&keywords=26%2Bawg%2Bsilicone&qid=1706329527&s=industrial&sprefix=26%2Bawg%2Bsilicon%2Cindustrial%2C225&sr=1-24&th=1) |
| USB OTG cable | This connects the SDS011 to the pi's USB input | [Pi Hut](https://thepihut.com/products/usb-otg-host-cable-microb-otg-male-to-a-female) |
| Solderable USB Power connectors | Use these to make the power cable for the LEDs | [Amazon](https://www.amazon.co.uk/Connector-Adapter-Socket-Welding-Breadboard-Black/dp/B091BQW8XC/ref=sr_1_3?keywords=usb+a+solder+connector&qid=1684496338&sprefix=usb+a+solder%2Caps%2C178&sr=8-3) |
| Bi-directional Level Shifter | The Arduino needs to be 5V to talk to the LEDs but the pi's logic level is 3.3V, this allows them to safely talk to each other over serial | [Pi Hut](https://thepihut.com/products/adafruit-4-channel-i2c-safe-bi-directional-logic-level-converter) |
| Pi zero perma proto board | This sits on top of the pi and has just enough space for, the Arduino and wires to connect the LEDs and the trigger | [Pi Hut](https://thepihut.com/products/adafruit-perma-proto-bonnet-mini-kit?variant=31955820881&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gclid=CjwKCAjw67ajBhAVEiwA2g_jENrbu3uQ6-omEA-A3tQTswgKykvILdj4CBNhBZS9y0BK_kT9_NemlBoCCVgQAvD_BwE) |
| SD card | For the pi, [an up to date disk image for the project is available here](https://drive.google.com/file/d/1RamosGUQSkOcT0gQoo1ZNAbDgKeyZLT0/view?usp=share_link) | [Amazon](https://www.amazon.co.uk/Micro-Card-MAGIX-Class10-Adapter/dp/B07LGCHSNC/ref=sr_1_2_sspa?crid=184GBPPOI0KLB&keywords=micro+sd+card&nav_sdd=aps&qid=1684936518&refinements=p_n_feature_browse-bin%3A411645031&rnid=411640031&s=computers&sprefix=micro+sd+&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) | 
| LED Strip Connectors | These are needed to make a detachable data cable to connect the Arduino as well as a power cable to connect the battery to the LEDs | [Pimoroni](https://shop.pimoroni.com/products/led-strip-input-output-cable-4-pin?variant=31374638841939) |
| Trigger Button | Any push to make button will do but this one sits nicely in the palm and gets me into trouble in airports | [Amazon](https://www.ebay.co.uk/itm/183489050436?hash=item2ab8ccb744:g:~o8AAOSwH~Rbxd9s&amdata=enc%3AAQAIAAAA4DfdPIFduKhGQRBQqlutzerEKH9%2F6RNEZjn3Z1kiBCsYGR2ctrjclE3IUXqcaRgGcd21BOHa8dMSrNRLMSEdcvR8hGgifm7HTiAZDQQih%2BLAFkMDMtJ8I9nYrIM86AtwnPZPUj%2FCxqeo3dGiAmnypXUPrJp%2Baf69Xn0eZk9wmZ5floXd1YFs6a98tY8XZKHJsaQf9BK%2BfcbMPeeyZsW8JzsuVzeOx4bIH%2Fivni9QvIrsGG6%2FrnSxfQxfX3YroEnApZ4l475Ea4DLF8OX38hkdSGBovgHLPW%2B1ZgKeda6qsnL%7Ctkp%3ABk9SR_Tg-uKJYg) |
| 1m Micro USB Cable | Connects and powers the pi from the battery pack, you probably have ten lying around already | [Pi Hut](https://thepihut.com/products/usb-to-micro-usb-cable-0-5m?variant=37979679293635) | 
| Wrist strap | This is really a phone holder for runners but it provides a handy surface to hotglue electronic components to in order to make them "wearable". I invite readers to arrive at their own solutions | [Amazon](https://www.amazon.co.uk/dp/B08X7FX673?psc=1&ref=ppx_yo2ov_dt_b_product_details)|
| Arduino Pro Mini (5V version) | [Cool Components](This programs the LEDs better than the pi can | https://coolcomponents.co.uk/products/arduino-pro-mini-328-3-3v-8mhz?_pos=3&_sid=6a4299cc2&_ss=r) |


## Circuit Diagam 
![Fritzing Circuit Diagram](../images/fritzing-circuit-diagram.png)

## Build instructions

1. Prepare pi by soldering header strip
2. Solder Arduino and level shifter (or just header strip and tape depending how confident you feel)
3. Solder all jumper wires on perma proto board
4. Solder connector to LED data cable 
5. Make LED data and power cables
6. Solder button
7. Flash Arduino with code provided
8. Flash pi sd with this image 
9. Test and pray


