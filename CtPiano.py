import sys
import pygame
import os
import pygame.midi
import pygame.mixer
import pyaudio
import array
import math
import time
from time import sleep

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,500),pygame.RESIZABLE)
pygame.display.set_caption("Chadtech v4.00 : CtPiano",)

sidebar = pygame.image.load('sidebar.PNG').convert()
deviceOptionBox = pygame.image.load('deviceoptionbox.PNG').convert()
selectedOption = pygame.image.load('selectedoption.png').convert()
okay = pygame.image.load('okay.png').convert()
#okaySelected = pygame.image.load('okaySelected.png').convert()

tones = [
1.0, # 1/1
1.16667, # 7/6
1.3125, # 21/16
1.375, # 11/8
1.5, # 3/2
1.75, # 7/4
1.83333, # 11/6
]


deviceChoice = 'None'
scaleChoice = 'None'
timbreChoice = 'None'

timbreOptions = ['Bars','Miscpercus','Triangledrop','Losaw','Hisaw','Losquare','DKsquare','Emphaenharm']
scaleOptions = ['Fauxslendro','Ptolemy 11lmt', 'JIT Europe', 'Doty OMJ14', 'Richoctave']

scaleTones = {
	'Fauxslendro':['1/1','7/6','4/3','32/21','7/4','2/1'],
	'Ptolemy 11lmt':['1/1','7/6','21/16','11/8','3/2','7/4','11/6'],
	'JIT Europe':['1/1','16/15','9/8','6/5','5/4','4/3','45/32','3/2','5/3','8/5','16/9','15/8','2/1'],
	'Doty OMJ14':['1/1','15/14','9/8','7/6','5/4','9/7','4/3','7/5','3/2','14/9','5/3','7/4','15/8','27/14','2/1'],
	'Richoctave':['1/1','21/20','10/9','7/6','6/5','5/4','9/7','21/16','10/7','40/27','14/9','8/5','5/3','12/7','9/5','40/21','2/1']
}


alternateNotation = {
	'Fauxslendro':['1','2','3','5','6'],
	'Ptolemy 11lmt':['None','None','None','None','None','None','None'],
	'JIT Europe':['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'],
	'Doty OMJ14':['None','None','None','None','None','None','None','None','None','None','None','None','None','None'],
	'Richoctave':['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
}

JITEuropeNotation = {
	'1/1','C'
	'16/15','C#'
	'9/8','D'
	'6/5','D#'
	'5/4','E'
	'4/3','F'
	'45/32','F#'
	'3/2','G'
	'5/3','G#'
	'8/5','A'
	'16/9','A#'
	'15/8','B'
}

#inp = pygame.midi.Input(1)


##### These Booleans permit different stages of the programming to while loop

selecting0 = True
selecting1 = True
selecting2 = True
mainLoop = True
quit = False

#### Loop to select input device
while selecting0 and not quit:
	screen.blit(sidebar,[0,0])
	screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Select input device',False,(192,192,192)),[180,32])
	for inputDeviceNumber in range(pygame.midi.get_count() ):
		#### blit the device options 
		screen.blit(deviceOptionBox,[180,(24*inputDeviceNumber)+50])
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render(str(pygame.midi.get_device_info(inputDeviceNumber)[1]),False,(192,192,192)),[182,(24*inputDeviceNumber)+54])
	#### If an option is selected, blit the gray selected box
	if type(deviceChoice)==int:
		screen.blit(selectedOption,[180,(24*deviceChoice)+50])
		screen.blit(okay,[180,(24*(pygame.midi.get_count()))+50])

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				if type(deviceChoice) == str:
					deviceChoice = 0
				elif type(deviceChoice) == int:
					if deviceChoice<pygame.midi.get_count()-1:
						deviceChoice+=1
			if event.key == pygame.K_UP:
				if type(deviceChoice) == str:
					deviceChoice = 0
				elif type(deviceChoice) == int:
					if deviceChoice>0:
						deviceChoice-=1
			if event.key == pygame.K_RETURN:
				if type(deviceChoice)==int:
					selecting0=False

		if event.type==pygame.MOUSEBUTTONDOWN:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<pygame.midi.get_count() and choiY>=0:
					deviceChoice=choiY

		if event.type==pygame.MOUSEBUTTONUP:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<pygame.midi.get_count() and choiY>=0:
					if type(deviceChoice)==int:
						selecting0=False


			if mouY>((pygame.midi.get_count()*24)+54) and mouY<((pygame.midi.get_count()*24)+78) and mouX>180 and mouX<236:
				if type(deviceChoice)==int:
					selecting0 = False

		if event.type == pygame.QUIT:
			selecting0 = False
			quit = True

	pygame.display.flip()
	clock.tick(44100)

inp = pygame.midi.Input(deviceChoice)
screen.fill((0,0,0))

#### Select scale options
while selecting1 and not quit:
	screen.fill((0,0,0))	
	screen.blit(sidebar,[0,0])
	screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Select scale',False,(192,192,192)),[180,32])
	for scaleNumber in range(len(scaleOptions)):
		#### blit the device options 
		screen.blit(deviceOptionBox,[180,(24*scaleNumber)+50])
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render(scaleOptions[scaleNumber],False,(192,192,192)),[182,(24*scaleNumber)+54])

	if type(scaleChoice)==int:
		screen.blit(selectedOption,[180,(24*scaleChoice)+50])
		screen.blit(okay,[180,(24*(len(scaleOptions)))+50])
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Tones in scale',False,(192,192,192)),[180,198])
		for toneNumber in range(len(scaleTones[scaleOptions[scaleChoice]])):
			screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render(scaleTones[scaleOptions[scaleChoice]][toneNumber]+',',False,(192,192,192)),[180+(84*(toneNumber%9)),222+(24*(toneNumber/9))])

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				if type(scaleChoice) == str:
					scaleChoice = 0
				elif type(scaleChoice) == int:
					if scaleChoice<len(scaleOptions)-1:
						scaleChoice+=1
			if event.key == pygame.K_UP:
				if type(scaleChoice) == str:
					scaleChoice = 0
				elif type(scaleChoice) == int:
					if scaleChoice>0:
						scaleChoice-=1
			if event.key == pygame.K_RETURN:
				if type(scaleChoice)==int:
					selecting1=False

	if event.type==pygame.MOUSEBUTTONDOWN:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<len(scaleOptions) and choiY>=0:
					scaleChoice=choiY

	if event.type==pygame.MOUSEBUTTONUP:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<len(scaleOptions) and choiY>=0:
					if type(scaleChoice)==int:
						selecting1=False

			if mouY>((len(scaleOptions)*24)+54) and mouY<((len(scaleOptions)*24)+78) and mouX>180 and mouX<236:
				if type(scaleChoice)==int:
					selecting1 = False

	if event.type == pygame.QUIT:
		selecting1 = False
		quit = True	

	pygame.display.flip()
	clock.tick(44100)

#### Select timbre options
while selecting2 and not quit:
	screen.fill((0,0,0))	
	screen.blit(sidebar,[0,0])
	screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Select Timbre',False,(192,192,192)),[180,32])
	for timbreNumber in range(len(timbreOptions)):
		#### blit the device options 
		screen.blit(deviceOptionBox,[180,(24*timbreNumber)+50])
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render(timbreOptions[timbreNumber],False,(192,192,192)),[182,(24*timbreNumber)+54])

	if type(timbreChoice)==int:
		screen.blit(selectedOption,[180,(24*timbreChoice)+50])
		screen.blit(okay,[180,(24*(len(timbreOptions)))+50])
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Wave form',False,(192,192,192)),[180,270])
		#for toneNumber in range(len(scaleTones[scaleOptions[scaleChoice]])):
		#	screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render(scaleTones[scaleOptions[scaleChoice]][toneNumber]+',',False,(192,192,192)),[180+(84*(toneNumber%9)),222+(24*(toneNumber/9))])

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				if type(timbreChoice) == str:
					timbreChoice = 0
				elif type(timbreChoice) == int:
					if timbreChoice<len(timbreOptions)-1:
						timbreChoice+=1
			if event.key == pygame.K_UP:
				if type(timbreChoice) == str:
					timbreChoice = 0
				elif type(timbreChoice) == int:
					if timbreChoice>0:
						timbreChoice-=1
			if event.key == pygame.K_RETURN:
				if type(timbreChoice)==int:
					selecting2=False
					screen.fill((0,0,0))
					screen.blit(sidebar,[0,0])
					screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Loading',False,(192,192,192)),[180,32])

	if event.type==pygame.MOUSEBUTTONDOWN:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<len(timbreOptions) and choiY>=0:
					timbreChoice=choiY

	if event.type==pygame.MOUSEBUTTONUP:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<len(timbreOptions) and choiY>=0:
					if type(timbreChoice)==int:
						selecting2 = False

			if mouY>((len(timbreOptions)*24)+54) and mouY<((len(timbreOptions)*24)+78) and mouX>180 and mouX<236:
				if type(timbreChoice)==int:
					selecting2 = False
					screen.fill((0,0,0))
					screen.blit(sidebar,[0,0])
					screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Loading',False,(192,192,192)),[180,32])


	if event.type == pygame.QUIT:
		selecting2 = False
		quit = True	

	pygame.display.flip()
	clock.tick(44100)

screen.fill((0,0,0))
screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',16).render('Loading',False,(192,192,192)),[180,32])

tones=[]
os.chdir(os.path.abspath(scaleOptions[scaleChoice]+' '+timbreOptions[timbreChoice]))
for yit in os.listdir(os.getcwd()):
	if  yit.endswith('.wav'):
		tones.append(pygame.mixer.Sound(yit))
os.chdir(os.path.dirname(os.getcwd()))

screen.fill((0,0,0))

printInfo = [['Tone Fraction      : ','NA'],['Alternate Notation : ','NA'],['Midi Number        : ', 'NA'],['Velocity           : ','NA']]

while mainLoop and not quit:

	screen.blit(sidebar,[0,0])

	for event in pygame.event.get():
		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_a:

		if event.type == pygame.QUIT:
			mainLoop = False

###### [[(144 if its a down press, 128 if its up), Midi note, (velocity, where 127 is loudest. Always 127 when up press) ], Time of event]
###### 0 is the bottom midi note (C), 120 is the top (if)

###### Gonna make three scales
	for infoType in range(len(printInfo)):
		screen.blit(pygame.font.Font('Command-Prompt-12x16.ttf',32).render(printInfo[infoType][0]+printInfo[infoType][1],False,(192,192,192)),[180,32 + (36*infoType)])

	if inp.poll():
		keys = inp.read(1000)
		for keyPressed in keys:
			pressData = keyPressed[0]
			#print pressData
			pressDirection = pressData[0]
			midiNumber = pressData[1]
			velocity = pressData[2]
			if pressDirection==144:
				printInfo[0][1] = scaleTones[scaleOptions[scaleChoice]][midiNumber%(len(scaleTones[scaleOptions[scaleChoice]])-1)]
				printInfo[1][1] = alternateNotation[scaleOptions[scaleChoice]][midiNumber%(len(scaleTones[scaleOptions[scaleChoice]])-1)]
				printInfo[2][1] = str(midiNumber)
				printInfo[3][1] = str(velocity).zfill(3)
				tones[midiNumber].set_volume((velocity/127.)**(3))
				tones[midiNumber].play()
				#tones[midiNumber].fadeout(int(5000*((velocity/127.))))
			elif pressDirection==128:
				#tones[midiNumber].stop()
				tones[midiNumber].fadeout(30)
	


	pygame.display.flip()
	clock.tick(44100)

	screen.fill((0,0,0))

pygame.quit()