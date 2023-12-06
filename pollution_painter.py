#!/usr/bin/python
#POLLUTION PAINTER - 'MAKING THE INVISIBLE VISIBLE' SINCE 2017!
#ROBIN PRICE 2017-2023

import time, os, sys, threading, zmq, struct
import RPi.GPIO as GPIO
from sds011lib import SDS011QueryReader
from serial import Serial
from datetime import datetime
from collections import deque
from scipy import interpolate
import numpy as np
from typing import List, Any
from time import sleep

class PollutionPainter:
	trigger_switch_pin = 6
	zmq_context = None
	zmq_socket = None
	got_brightness = False
	brightness = 30
	got_wait = False
	wait = 10
	got_fade = False
	fade = 1000
	sensor = None
	arduino_port = None
	sending_to_arduino = False
	currently_drawing = False
	just_started = False
	just_stopped = False
	dummy_mode = False
	dummy_pm25 = 0

	pm25 = 0
	buff = deque(np.zeros(5, dtype='f'), 5)
	tbuff = deque(np.zeros(5, dtype='f'), 5)
	x_points = np.linspace(0,550, num=256, endpoint=False)
	y_points = np.linspace(255,45, num=256, endpoint=False)

	def __init__(self):
		try:
			#TRIGGER BUTTON SETUP
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(self.trigger_switch_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
			GPIO.add_event_detect(self.trigger_switch_pin, GPIO.FALLING, callback=self.trigger_callback, bouncetime=1000)

			#SENSOR SETUP
			self.sensor = SDS011QueryReader('/dev/ttyUSB0')

			#ARDUINO SERIAL LINK SETUP
			self.arduino_port = Serial("/dev/ttyAMA0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0)

		except Exception as e:
			print ("Startup Error: {}".format(e))

	def run(self):
		try:
			#START SAMPLING
			self.sample()
			
			#START TALKING TO LED
			self.control_LEDS()
			
			#HANDLE WEB FRONT END
			self.handle_zmq()

		except:
			GPIO.cleanup()

	def trigger_callback(self,arg):
		print("button {} pressed".format(str(self.trigger_switch_pin)))
		if self.currently_drawing:
			self.currently_drawing = False
			self.just_stopped = True
		else:
			self.currently_drawing = True
			self.just_started = True

	def sample(self):
		threading.Timer(1.0, self.sample).start()
		aqi = self.sensor.query()
		if (aqi.pm25):
			print("PM2.5 " + str(aqi.pm25) + " ug/m^3")
			self.pm25 = aqi.pm25
			self.tbuff.append(time.time())
			self.buff.append(aqi.pm25)

	def control_LEDS(self):
		threading.Timer(1.0, self.control_LEDS).start()
		if not self.sending_to_arduino:
			if self.just_started:
				self.command_out("<start>")
				self.just_started = False
			if self.just_stopped:
				self.command_out("<stop>")
				self.just_stopped = False
			if self.got_brightness:
				self.command_out("<brightness " + str(self.brightness).zfill(3) + ">")
				self.got_brightness = False
			if self.got_wait:
				self.command_out("<wait " + str(self.wait).zfill(3) + ">")
				self.got_wait = False
			if self.got_fade:
				self.command_out("<fade " + str(self.fade).zfill(4) + ">")
				self.got_fade = False

			interpolated_pm25 = (self.f(time.time() - 1, self.buff, self.tbuff))
			print("interpolated_pm25 = {}".format(interpolated_pm25))
			if (self.dummy_mode == True):
				interpolated_PM25 = self.dummy_pm25
			cutoff=int(np.interp(interpolated_pm25, self.x_points, self.y_points))
			self.command_out("<cutoff " + str(cutoff).zfill(3) + ">")
		else:
			print("already sending")

	def command_out(self, command):
		self.sending_to_arduino = True
		correct_response = False
		attempts = 0
		while correct_response == False and attempts < 8:
			print("sending " + command)
			self.arduino_port.flushInput()
			self.arduino_port.flushOutput()
			bytes_out = self.arduino_port.write(command.encode('utf-8'))
			attempts = attempts + 1
			sleep(0.1)
			response = "<" + self.arduino_port.read(bytes_out).decode('utf-8') + ">"
			print("got response " + response)
			if response == command:
				correct_response = True
		if not correct_response:
			print("failed to send {} to arduino".format(command))
		self.sending_to_arduino = False

	def handle_zmq(self):		
		#LISTEN FOR ZMQ FROM WYSGI TO SERVE WEB FRONT END
		self.zmq_context = zmq.Context()
		self.zmq_socket = self.zmq_context.socket(zmq.REP)
		self.zmq_socket.bind("tcp://*:5555")
		while True:
			try:
				message = self.zmq_socket.recv_multipart()
				if (message[0] == b'get_pm25'):
					print("get_pm25 request sending pm25 = {}".format(str(self.pm25)))
					ba = bytearray(struct.pack("f", self.pm25))
					self.zmq_socket.send(ba)
				elif (message[0] == b'set_brightness'):
					self.brightness = struct.unpack('i', message[1])[0]
					print("set_brightness request setting brightness = {}".format(str(self.brightness)))
					self.zmq_socket.send(b'msg_rxd')
					self.got_brightness = True
				elif (message[0] == b'set_fade'):
					self.fade = struct.unpack('i', message[1])[0]
					print("set_fade request setting fade = {}".format(str(self.fade)))
					self.zmq_socket.send(b'msg_rxd')
					self.got_fade = True
				elif (message[0] == b'set_refresh'):
					self.wait = struct.unpack('i', message[1])[0]
					print("set_refresh request setting wait = {}".format(str(self.wait)))
					self.zmq_socket.send(b'msg_rxd')
					self.got_wait = True
			except Exception as err:
				print(Exception, err)
				print("error in zmq request")

	def f(self, x, b, t):
		y_points = np.array(list(b))
		x_points = np.array(list(t))
		return np.interp(x, x_points, y_points)

if __name__ == '__main__':
	user = os.getuid()
	if user != 0:
		print("Please run script as root")
		sys.exit()

	painter = PollutionPainter()
	painter.run()

#CODE BELOW IS LEGACY REMINDER CODE 


def manualmode_handler(address: str, *args: List[Any]) -> None:
	print(address)
	print(args)
	print(len(args))
	print(type(args[0]))
	print(type(args[1]))
	if not len(args)== 1 or type(args[0]) is not float:
		global DUMMY_MODE
		if args[1] == 1:
			DUMMY_MODE = True
			print("set DUMMY_MODE = True")
		else:
			DUMMY_MODE = False
			print("set DUMMY_MODE = False")

def manualPM25_handler(address: str, *args: List[Any]) -> None:
	if not len(args)== 1 or type(args[0]) is not float:
		global DUMMY_PM25
		DUMMY_PM25 = int(args[1])
		print("recieved OSC /manualPM25 {}".format(DUMMY_PM25))
		client.send_message("/manualPM25", DUMMY_PM25)