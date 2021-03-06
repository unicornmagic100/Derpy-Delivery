"""
Copyright 2010 Erik Soma <stillusingirc@gmail.com>

This file is part of Derpy Delivery.

Derpy Delivery is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Derpy Delivery is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Derpy Delivery. If not, see <http://www.gnu.org/licenses/>.
"""

import pygame

#handles keyboard input
class handler():
	
	def __init__(self):
		self.keyRelease = {}
		self.keyDown = {}
		self.keyPress = {}
		self.down = {}
		self.joysticks = []
		self.getJoysticks()
			
	
	#assignKeyRelease
	#	arguments:
	#		keyEvent 	- key code
	#		task		- function to execute when key is released
	def assignKeyRelease(self, keyEvent, task):
		strKeyEvent = str(keyEvent)
		if task is not None:
			self.keyRelease[strKeyEvent] = task
		else:
			if strKeyEvent in self.keyRelease:
				del self.keyRelease[strKeyEvent]
				
	#assignKeyDown
	#	arguments:
	#		keyEvent 	- key code
	#		task		- function to execute when key is down
	def assignKeyDown(self, keyEvent, task):
		strKeyEvent = str(keyEvent)
		if task is not None:
			self.keyDown[strKeyEvent] = task
		else:
			if strKeyEvent in self.keyDown:
				del self.keyDown[strKeyEvent]
				
	#assignKeyPress
	#	arguments:
	#		keyEvent 	- key code
	#		task		- function to execute when key is pressed
	def assignKeyPress(self, keyEvent, task):
		strKeyEvent = str(keyEvent)
		if task is not None:
			self.keyPress[strKeyEvent] = task
		else:
			if strKeyEvent in self.keyPress:
				del self.keyPress[strKeyEvent]
	
	#process when a press happens
	#	arguments:
	#		event - pygame key/joybutton event
	def processPress(self, event):
		if event.type == pygame.JOYBUTTONDOWN:
			key = (self.joysticks[event.joy].get_name()).replace(" ", "") + "_" + str(event.button)
		else:
			key = str(event.key)
		self.down[key] = True	#set the key to down
		if key in self.keyPress:
			self.keyPress[key]()
			
	#process when a release happens
	#	arguments:
	#		event - pygame key/joybutton event
	def processRelease(self, event):
		if event.type == pygame.JOYBUTTONUP:
			key = (self.joysticks[event.joy].get_name()).replace(" ", "") + "_" + str(event.button)
		else:
			key = str(event.key)
		del self.down[key]		#remove the key from down position
		if key in self.keyRelease:
			self.keyRelease[key]()
			
	#process when analog axis motion happens
	#	arguments:
	#		event - pygame joyaxis motion event
	def processAnalog(self, event):
		key = (self.joysticks[event.joy].get_name()).replace(" ", "") + "_"+str(event.axis)+"_axis"
		if event.value > -.5 and event.value < .5: 	#release
			if key+"_1" in self.down:
				del self.down[key+"_1"]		#remove the key from down position
				if key+"_1" in self.keyRelease:
					self.keyRelease[key+"_1"]()
			if key+"_-1" in self.down:
				del self.down[key+"_-1"]		#remove the key from down position
				if key+"_-1" in self.keyRelease:
					self.keyRelease[key+"_-1"]()
		else:										#press
			if event.value > 0:
				self.down[key+"_1"] = True	#set the key to down
				if key+"_1" in self.keyPress:
					self.keyPress[key+"_1"]()
				if key+"_-1" in self.down:
					del self.down[key+"_-1"]		#remove the key from down position
					if key+"_-1" in self.keyRelease:
						self.keyRelease[key+"_-1"]()
			else:
				self.down[key+"_-1"] = True	#set the key to down
				if key+"_-1" in self.keyPress:
					self.keyPress[key+"_-1"]()
				if key+"_1" in self.down:
					del self.down[key+"_1"]		#remove the key from down position
					if key+"_1" in self.keyRelease:
						self.keyRelease[key+"_1"]()

	#processes all pressed keys
	def process(self):
		for key in self.down:
			if key in self.keyDown:
				self.keyDown[key]()
				
				
	def keyCodeToString(self, keyCode):
		if keyCode.isdigit():
			keyCode = int(keyCode)
			return pygame.key.name(keyCode)
		else:
			return keyCode
		
	def getJoysticks(self):
		for j in self.joysticks:
			j.quit()
		self.joysticks = []
		pygame.joystick.quit()
		pygame.joystick.init()
		if pygame.joystick.get_count() > 0:
			for i in range(pygame.joystick.get_count()):
				duplicate = False
				joystick = pygame.joystick.Joystick(i)
				joystick.init()
				for j in self.joysticks:
					if j.get_name == joystick.get_name:
						duplicate = True
				if not duplicate:
					self.joysticks.append(joystick)
				else:
					self.joysticks.quit()
		