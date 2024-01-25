This is just a fritzing to show how I wire the arduino to the raspberry pi using a bi directional level shifter
for the serial connection in case the instructions aren't enough. It shows the LEDS too. The SDS0111 pollution 
sensor isn't in the diagram because it's connected to the pi's usb port and fritzing can't handle that. It 
also displays a AA battery for the LEDS, in reality I use a 2.4A fast charge 5V USB battery pack with two ports, 
one connected to the pi and the other the LEDS.

I've only connected the relelvant pins on the pi to the perma proto in the diagram even though in reality they're
all connected. The relevant pins are 5V, 3.3V, GND, RX/TX and GPIO BCM 6.
