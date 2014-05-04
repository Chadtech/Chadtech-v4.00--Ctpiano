import os
import math
import random
import struct
import wave

tones = [
1.0, # 1/1
1.06667, # 16/15
1.125, # 9/8
1.2, # 6/5
1.25, # 5/4
1.33333, # 4/3
1.40625, # 45/32
1.5, # 3/2
1.6, # 8/5
1.66667, # 5/3
1.77778, # 16/9
1.875, # 15/8
]

sampleRate = 44100.
amp = 32767
oneSec = 1000.
noteDiv = 12
barNum = 4
noteDur = 6000 # time length of note in thousandths of a second
noteCou = 4 #Number of notes per bar
percent = 0
speedOfSound = 340.49/sampleRate
songDur = (barNum*(noteDur/oneSec))*sampleRate
fileName = ''

def makeArray(dur): # Makes an empty array with the length given (dur) in notes of time length noteDur and sample length of noteDur/1000 * sampleRate
	outRay = []
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for vapp in range(inDur):
		outRay.append(0)
	return outRay

def makeTone(tone,dur): #Returns an array of a given tone, for a certain duration
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for vapp in range(inDur):
		value = math.sin((vapp*2*math.pi*inTone))*amp
		values[vapp] = value
	return values

def makeSaw(tone,dur): #Make a saw tooth wave
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for vapp in range(inDur):
		#print (vapp%inTone)*(2*amp), vapp, inTone, vapp%inTone
		value = (amp - (((vapp*tone)%(sampleRate))/sampleRate)*amp) - (amp/2)
		#value = (-(2*amp)/math.pi)*math.atan(1/math.tan((vapp*math.pi)/inTone))
		values[vapp]=value
	return values

def combineWavs(whereAt,durRay,songRay,level): #whereAt is (WhichBar, which of noteDiv*barNum in whichbar), function adds input array to song array starting at whereAt. 
	whereAtIn = whereAt*(noteDur/oneSec)*sampleRate
	for vapp in range(len(durRay)):
		songRay[vapp+int(whereAtIn)] += durRay[vapp] *(level/1000.)

def volDrop(durRay,volPert): #Change the volume for an array as a whole values less than 1000 will lower the volume
	inRay = durRay
	outRay = []
	volPert = volPert/1000.
	percent = 0
	for vapp in range(len(inRay)):
		outRay.append(inRay[vapp]*volPert)
		if vapp%((int(len(inRay)))/100)==0:
			percent += 1
			print percent, '%', 'volDrop'
	return outRay

def buildFile(song, name): #Turns input 'song' into .wav file.
	fileName = name
	noise_output = wave.open(fileName, 'w')
	noise_output.setparams((1, 2, sampleRate, 0, 'NONE', 'not compressed'))	
	percent = 0
	for yit in range(len(song)):
		if song[yit] < 32767 and song[yit] > -32767:
			packed_value = struct.pack('h', (song[yit]))
			noise_output.writeframes(packed_value)
			if yit%(int(len(song))/100)==0:
				percent += 1
				print percent, '%', song[yit]
		else:
			if song[yit] >= 32767:
				packed_value = struct.pack('h', 32767)
				noise_output.writeframes(packed_value)
				if yit%(int(len(song))/100)==0:
					percent += 1
					print percent, '%', song[yit]
			if song[yit] <= -32767:
				packed_value = struct.pack('h', -32767)
				noise_output.writeframes(packed_value)
				if yit%(int(len(song))/100)==0:
					percent += 1
					print percent, '%', song[yit]
	print fileName, 'is done'
	noise_output.close()

for yit in range(0,127):
	thisTone = makeArray(9)
	frequency = tones[yit%len(tones)]*25*(2**(yit/len(tones)))

	print 'TONE:', tones[yit%len(tones)], ', MIDI NUMBER: ', yit

	combineWavs(0,makeTone(frequency,8),thisTone,800.)

	buildFile(thisTone,str(frequency)+'.wav')
