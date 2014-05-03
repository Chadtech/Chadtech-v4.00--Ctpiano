import sys
import pygame
import os
import pygame.midi
import pygame.mixer

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.midi.init()

screen = pygame.display.set_mode((1000,500),pygame.RESIZABLE)
pygame.display.set_caption("ChadTech That Does Sound",)

for yit in range(pygame.midi.get_count() ):
    print pygame.midi.get_device_info(yit), yit

ONon = pygame.mixer.Sound('800b.wav')

inp = pygame.midi.Input(1)

goin = True

while goin:

    for event in pygame.event.get():    
        if event.type == pygame.KEYDOWN:
            if event.key:
                if event.key==113:
                    goin=False

######  [[(144 if its a down press, 128 if its up), Midi note, (velocity, where 127 is loudest. Always 127 when up press) ], Time of event]

    if inp.poll():
            keys = inp.read(1000)
            print keys
            if keys[0][0][2] != 127:
                ONon.play()