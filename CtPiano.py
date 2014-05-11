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
deviceOptionBox = pygame.image.load('deviceoptionbox.PNG').convert()
selectedOption = pygame.image.load('selectedoption.png').convert()
okay = pygame.image.load('okay.png').convert()
#okaySelected = pygame.image.load('okaySelected.png').convert()


deviceChoice = 'None'
scaleChoice = 'None'
timbreChoice = 'None'

timbreOptions = ['Bars','Miscpercus','Triangledrop','Lowsaw','Hisaw','Losquare','DKsquare','Emphaenharm']
scaleOptions = ['Fauxslendro','Ptolemy 11 lmt', 'JIT Europe', 'Doty OMJ14', 'Richoctave']

scaleTones = {
	'Fauxslendro':['1/1','7/6','4/3','32/21','7/4','2/1'],
	'Ptolemy 11 lmt':['1/1','7/6','21/16','11/8','3/2','7/4','11/6','2/1'],
	'JIT Europe':['1/1','16/15','9/8','6/5','5/4','4/3','45/32','3/2','5/3','8/5','16/9','15/8','2/1'],
	'Doty OMJ14':['1/1','15/14','9/8','7/6','5/4','9/7','4/3','7/5','3/2','14/9','5/3','7/4','15/8','27/14','2/1'],
	'Richoctave':['1/1','21/20','10/9','7/6','6/5','5/4','9/7','21/16','10/7','40/27','14/9','8/5','5/3','12/7','9/5','40/21','2/1']
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

		if event.type==pygame.MOUSEBUTTONUP:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<pygame.midi.get_count() and choiY>=0:
					deviceChoice=choiY

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
						scaleChoice+=1
			if event.key == pygame.K_UP:
				if type(timbreChoice) == str:
					timbreChoice = 0
				elif type(timbreChoice) == int:
					if timbreChoice>0:
						timbreChoice-=1
			if event.key == pygame.K_RETURN:
				if type(timbreChoice)==int:
					selecting2=False

	if event.type==pygame.MOUSEBUTTONDOWN:
			mouX,mouY = event.pos
			choiY = (mouY-50)/24
			if mouX>=180 and mouX<953:
				if choiY<len(timbreOptions) and choiY>=0:
					timbreChoice=choiY

			if mouY>((len(timbreOptions)*24)+54) and mouY<((len(timbreOptions)*24)+78) and mouX>180 and mouX<236:
				if type(timbreChoice)==int:
					selecting2 = False

	if event.type == pygame.QUIT:
		selecting2 = False
		quit = True	

	pygame.display.flip()
	clock.tick(44100)

screen.fill((0,0,0))

tones=[]
os.chdir(os.path.abspath('Faux Slendro Bars'))
for yit in os.listdir(os.getcwd()):
	if  yit.endswith('.wav'):
		tones.append(pygame.mixer.Sound(yit))
os.chdir(os.path.dirname(os.getcwd()))

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