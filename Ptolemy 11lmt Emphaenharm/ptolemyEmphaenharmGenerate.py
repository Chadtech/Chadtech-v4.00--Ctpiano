import os
import math
import random
import struct
import wave
import time

tones = [
1.0, # 1/1
1.16667, # 7/6
1.3125, # 21/16
1.375, # 11/8
1.5, # 3/2
1.75, # 7/4
1.83333, # 11/6
]

sampleRate = 44100.
amp = 32767
oneSec = 1000.
noteDiv = 12
barNum = 4
noteDur = 6000 # time length of note in thousandths of a second
noteCou = 4 #Number of notes per bar
percent = 0
songDur = (barNum*(noteDur/oneSec))*sampleRate
fileName = ''

def makeArray(dur): # Makes an empty array with the length given (dur) in notes of time length noteDur and sample length of noteDur/1000 * sampleRate
	outRay = []
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for vapp in range(inDur):
		outRay.append(0)
	return outRay

def volSlop(durRay,volSlop): # Add a volume slope to an array. The higher the volume slope, the slower the the array reaches volume zero, or even increases in volume.
	inRay = durRay
	volSlop = (volSlop/1000. + 999.)/1000.
	for vapp in range(len(durRay)):
		inRay[vapp] = inRay[vapp]*(volSlop**vapp)
	return inRay

def makeTone(tone,dur,phase=0): #Returns an array of a given tone, for a certain duration
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for vapp in range(inDur):
		value = math.sin((vapp*2*math.pi*inTone + (phase * math.pi) ))*amp
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

def makeSawTrig(tone,dur): #Make a saw tooth wave
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for harmonic in range(harmNum):
		for vapp in range(len(values)):
			values[vapp]+= amp*((-1)**(harmonic))*(math.sin(vapp*2*math.pi*inTone*harmonic)/harmonic)
	return values

def makeTriangle(tone,dur): #Make a Triangle wave without trigonometry
	values = []
	inTone = float(tone/2)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for vapp in range(inDur):
		value = (amp - ((((vapp*(tone/2))%(sampleRate))/sampleRate)*amp) - (amp/2))
		values[vapp]=value
	for gno in range(len(values)):
		values[gno]=math.fabs(values[gno])
	for brs in range(len(values)):
		values[brs] = (values[brs]*2) - (amp/2)
	return values

def makeTriangleTrig(tone,dur,harmNum): #Make a Triangle Wave with trigonometry
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for harmonic in range(harmNum):
		for vapp in range(len(values)):
			values[vapp]+= amp*((-1)**(harmonic))*(math.sin(vapp*2*math.pi*inTone*((harmonic*2)+1))/(((harmonic*2)+1)**2))
	return values

def makeTriangleEnharmonic(tone,dur,harmNum): #Make a Triangle Wave with enharmonics
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for harmonic in range(harmNum):
		for vapp in range(len(values)):
			values[vapp]+= amp*((-1)**(harmonic))*(math.sin((1+(harmonic*(0.0007)))*vapp*2*math.pi*inTone*((harmonic*2)+1))/(((harmonic*2)+1)**2))
	return values

def makeTriangleEnharmonicMitDecay(tone,dur,harmNum): #Make a Triangle Wave with enharmonics
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for harmonic in range(harmNum):
		for vapp in range(len(values)):
			if harmonic>0:
				values[vapp]+= ((8481./(481.+(vapp*(harmNum))))*2*amp*((-1)**(harmonic))*(math.sin((1+(harmonic*(0.00007)))*vapp*2*math.pi*inTone*((harmonic*2)+1))/(((harmonic*2)+1)**2)))
			else:
				values[vapp]+= ((1-(8481./(8481.+(harmNum*3*vapp))))*amp*((-1)**(harmonic))*(math.sin((1+(harmonic*(0.00007)))*vapp*2*math.pi*inTone*((harmonic*2)+1))/(((harmonic*2)+1)**2)))
	return values

def makeTriangleEnharmonicMitDecayOn(tone,dur,harmNum): #Make a Triangle Wave with enharmonics
	values = []
	inTone = float(tone)/sampleRate
	inDur = int(float(dur)*(noteDur/oneSec)*(sampleRate))
	for yit in range(inDur):
		values.append(0.)
	for harmonic in range(harmNum):
		for vapp in range(len(values)):
			values[vapp]+= ((8481./(481.+(vapp*(harmNum))))*2*amp*((-1)**(harmonic))*(math.sin((1+(harmonic*(0.00007)))*vapp*2*math.pi*inTone*((harmonic*2)+1))/(((harmonic*2)+1)**2)))
	return values

def combineWavs(whereAt,durRay,songRay,level): #whereAt is (WhichBar, which of noteDiv*barNum in whichbar), function adds input array to song array starting at whereAt. 
	whereAtIn = whereAt*(noteDur/oneSec)*sampleRate
	for vapp in range(len(durRay)):
		songRay[vapp+int(whereAtIn)] += durRay[vapp] *(level/1000.)

def volDrop(durRay,volPert): #Change the 'volume' of an array, number values less than 1000 will lower the volume
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
	thisTone = makeArray(2.1)
	frequency = tones[(yit)%len(tones)]*25*(2**((yit)/len(tones)))

	print 'TONE:', tones[yit%len(tones)], ', MIDI NUMBER: ', yit

	combineWavs(0,volSlop(makeTriangleEnharmonic(frequency/2.,2,30),500.),thisTone,200.)
	combineWavs(0,volSlop(makeTriangleEnharmonic(frequency/4.,2,30),350.),thisTone,200.)
	combineWavs(0,volSlop(makeTriangleEnharmonic(frequency,2,30),600.),thisTone,200.)
	combineWavs(0,volSlop(makeTone(frequency,2),700.),thisTone,400.)

	
	buildFile(thisTone,str(yit).zfill(3)+'.wav')