import sys
import pygame
import os
import pygame.midi
import pygame.mixer

pygame.mixer.pre_init(44100, -8, 1, 512)
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,500),pygame.RESIZABLE)
pygame.display.set_caption("Chadtech v4.00 : CtPiano",)

welcomescreen = pygame.image.load('welcomescreen.PNG').convert()

for yit in range(pygame.midi.get_count() ):
    print pygame.midi.get_device_info(yit), yit


tones=[]
os.chdir(os.path.abspath('JIT Europe Sines'))

inp = pygame.midi.Input(1)
curTones = []

for yit in os.listdir(os.getcwd()):
    if  yit.endswith('.wav'):
        tones.append(pygame.mixer.Sound(yit))

goin = True
while goin:

    screen.blit(welcomescreen,[0,0])

    for event in pygame.event.get(): 

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
                tones[midiNumber].play()
            elif pressDirection==128:
                tones[midiNumber].stop()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
