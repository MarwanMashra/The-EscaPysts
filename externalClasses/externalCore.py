#!/bin/usr/python3
#-*-coding:utf8;-*-

from externalClasses.externalGraphics import *
from externalClasses.externalLevel import *
from externalClasses.externalPlayer import *
from externalClasses.externalMenu import *

class Core():
	"""classe prinicpale gérant toutes les autres"""

	graphicHandlerObject = Graphics(800,800)
	clock = pygame.time.Clock()
	
	def __init__(self, FPS_limit=240):
		self.fpsLimit = FPS_limit
		self.quit = False

		self.mainMenuHandlerObject = Menu(self.graphicHandlerObject)

			
	def keyLock(self):
		for x in self.keys:
			if x in self.keysRegister:
				if x != "U" and x !="D" and x !="L" and x !="R":
					self.keys.remove(x)
			else :
				if x != "U" and x !="D" and x !="L" and x !="R":
					self.keysRegister.append(x)
				
	def startLevel(self):
		self.levelHandlerObject = Level(self.graphicHandlerObject)
		self.playerHandlerObject = Player(self.graphicHandlerObject,self.levelHandlerObject,self.keys)
		for x in self.levelHandlerObject.ennemies :
			x.playerHandlerObject = self.playerHandlerObject
		self.levelHandlerObject.playerHandlerObject = self.playerHandlerObject
		self.mainMenuHandlerObject.buttonPressed[0] = False

	def run(self):

		run = True
		static = True #(menu)

		options = False
		play = False

		####### game loop
		while run:
			Core.clock.tick(self.fpsLimit) #defines clock's max speed by (1/FPS_limit) ms per frame
			self.keys = self.graphicHandlerObject.getKeys()

			try :
				temporaryKeyLock = self.keys[:]
				self.keyLock()
			
			except :
				####### game-ender
				if type(self.keys) == bool:
					run = not(self.keys)

			else :

				####### options menu trigger
				if "esc" in self.keys or options:
					if not options :
						self.optionsMenuHandlerObject = Menu(self.graphicHandlerObject)
						self.optionsMenuHandlerObject.buttonPressed, self.optionsMenuHandlerObject.buttonCoords, self.optionsMenuHandlerObject.buttonImages = [],[],[]
						self.optionsMenuHandlerObject.backgroundAdress = "images/options.png"

					self.optionsMenuHandlerObject.update()


					if "esc" in self.keys:
						if options and play:
							self.graphicHandlerObject.displayBackgroundUpdate(self.levelHandlerObject.imageAdress)
						options = not(options)

				####### main menu
				elif static:
					self.mainMenuHandlerObject.update()

				####### level trigger
				if (("ENTER" in self.keys or "Enter" in self.keys or self.mainMenuHandlerObject.buttonPressed[0]) or play) and not options:
					if not play:
						self.startLevel()
						play = True
						static = False
						# self.levelHandlerObject.test()
					if self.playerHandlerObject.death:
						self.startLevel()
					####### in-level actions :
					self.graphicHandlerObject.displayBackgroundUpdate()
					self.playerHandlerObject.keys = self.keys[:]
					self.playerHandlerObject.update()
					self.levelHandlerObject.update(self.fpsLimit)


				####### endLoop actions
				self.keysRegister = temporaryKeyLock[:]
				self.graphicHandlerObject.generalDisplayUpdate()

				####### tests zone
				
