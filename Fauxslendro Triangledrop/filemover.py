import os
import shutil

for wav in os.listdir(os.getcwd()):
	if wav.endswith('.wav'):
		if not wav.endswith('d.wav'):
			os.remove(wav)