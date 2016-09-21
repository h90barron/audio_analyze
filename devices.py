import pyaudio
import sys
import math

# Obtain list of local audio devices

def list_devices():
	p = pyaudio.PyAudio()
	i = 0
	n = p.get_device_count()
	while i < n:
		dev = p.get_device_info_by_index(i)
		if dev['maxInputChannels'] > 0:
			print(str(i) + '. ' + dev['name'])
		i = i + 1

if __name__ == '__main__':
	list_devices()
