import sys
import pygame
import os
import pygame.midi
import pygame.mixer
import pyaudio
import array
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,500),pygame.RESIZABLE)
pygame.display.set_caption("Chadtech v4.00 : CtPiano",)

sidebar = pygame.image.load('sidebar.PNG').convert()

for yit in range(pygame.midi.get_count() ):
	print pygame.midi.get_device_info(yit), yit

inp = pygame.midi.Input(1)

tones=[]
os.chdir(os.path.abspath('Faux Slendro Bars'))
for yit in os.listdir(os.getcwd()):
	if  yit.endswith('.wav'):
		tones.append(pygame.mixer.Sound(yit))
os.chdir(os.path.dirname(os.getcwd()))

##### These Booleans permit different stages of the programming to while loop

selecting = True
mainLoop = True
quit = False

while selecting and not quit:
	screen.blit(sidebar,[0,0])
	for inputDeviceNumber in range(pygame.midi.get_count() ):
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render(str(pygame.midi.get_device_info(inputDeviceNumber)[1]),False,(192,192,192)),[150,(16*inputDeviceNumber)+48])

	for event in pygame.event.get():
		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_a:

		if event.type == pygame.QUIT:
			selecting = False
			quit = True

	pygame.display.flip()
	clock.tick(44100)


while mainLoop and not quit:

	#screen.blit(welcomescreen,[0,0])

	for event in pygame.event.get():
		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_a:

		if event.type == pygame.QUIT:
			mainLoop = False

###### [[(144 if its a down press, 128 if its up), Midi note, (velocity, where 127 is loudest. Always 127 when up press) ], Time of event]
###### 0 is the bottom midi note (C), 120 is the top (if)

###### Gonna make three scales

	if inp.poll():
		keys = inp.read(1000)
		for keyPressed in keys:
			pressData = keyPressed[0]
			print pressData
			pressDirection = pressData[0]
			midiNumber = pressData[1]
			velocity = pressData[2]
			if pressDirection==144:
				tones[midiNumber].set_volume((velocity/127.)**(3))
				tones[midiNumber].play()
				#tones[midiNumber].fadeout(int(5000*((velocity/127.))))
			elif pressDirection==128:
				#tones[midiNumber].stop()
				tones[midiNumber].fadeout(30)

	pygame.display.flip()
	clock.tick(44100)

pygame.quit()