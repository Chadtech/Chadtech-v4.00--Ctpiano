import sys
import pygame
import os
import pygame.midi
import pygame.mixer
import pyaudio
import array
import math

pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,500),pygame.RESIZABLE)
pygame.display.set_caption("Chadtech v4.00 : CtPiano",)

welcomescreen = pygame.image.load('welcomescreen.PNG').convert()

p = pyaudio.PyAudio()
stream = p.open(rate=44100, channels=1, format=pyaudio.paFloat32, output=True)

for yit in range(pygame.midi.get_count() ):
	print pygame.midi.get_device_info(yit), yit

inp = pygame.midi.Input(1)

tones=[]
os.chdir(os.path.abspath('Faux Slendro Bars'))
for yit in os.listdir(os.getcwd()):
	if  yit.endswith('.wav'):
		tones.append(pygame.mixer.Sound(yit))

goin = True
while goin:

	screen.blit(welcomescreen,[0,0])

	for event in pygame.event.get():
		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_a:
		#		stream.write(array.array('f',(.25 * math.sin(i / 10.) for i in range(1000))).tostring())


		if event.type == pygame.QUIT:
			goin = False

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
				tones[midiNumber].fadeout(int(5000*((velocity/127.))))
			elif pressDirection==128:
				tones[midiNumber].stop()
				tones[midiNumber].fadeout(30)

	pygame.display.flip()
	clock.tick(44100)

pygame.quit()
#stream.close()
#p.terminate()

	