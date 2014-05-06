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
pygame.display.set_caption("Chadtech v4.00 : pyaudio practice",)

welcomescreen = pygame.image.load('welcomescreen.PNG').convert()

p = pyaudio.PyAudio()
stream = p.open(rate=44100, channels=1, format=pyaudio.paFloat32, output=True)

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in xrange(period)]
    return (lookup_table[i%period] for i in xrange(period))

toneFire = False
countDown = False
phasePosition = 0
volume = 100.
goin = True
while goin:

	screen.blit(welcomescreen,[0,0])

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				toneFire=True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				countDown=True
				phasePosition=0

		if event.type == pygame.QUIT:
			goin = False

	if toneFire==True:
		if countDown==False:
			stream.write(array.array('f',sine_wave(400)).tostring())
		else:
			stream.write(array.array('f',sine_wave(400, amplitude=volume/200.)).tostring())
			volume-=3
			if volume<0:
				toneFire=False
				countDown=False
				volume=100.

###### [[(144 if its a down press, 128 if its up), Midi note, (velocity, where 127 is loudest. Always 127 when up press) ], Time of event]
###### 0 is the bottom midi note (C), 120 is the top (if)

###### Gonna make three scales

	pygame.display.flip()
	clock.tick(44100)

pygame.quit()
stream.close()#p.terminate()

