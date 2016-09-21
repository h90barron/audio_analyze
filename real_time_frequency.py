import pyaudio
import wave
from scipy.io import wavfile
from scipy.fftpack import fft
from pylab import*

# This is intended to be used with a constant audio frequency.
# Analyzing the audio in the same loop as it is collected will 
# cause issue when sampling from anything but a constant frequency
# since the operations  will delay subsequent samplings. 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "output.wav"
DEVICE = 2

p = pyaudio.PyAudio()
file = open("raw_data.txt", 'a')
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
		input_device_index=DEVICE)

print("* recording")

frames = []
frequency_data = []

# Sample converted to nparray for FFT

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#for i in range(1):
    data = stream.read(CHUNK)
    decoded = np.fromstring(data, dtype=np.int32)
    coef = decoded.flatten()
    print(coef)
    raw_data = [(x/2**8.)*2-1 for x in coef]
    raw_transform = fft(raw_data)
    freqs = fftfreq(len(raw_transform))
    idx = np.argmax(np.abs(raw_transform))
    #print(freqs)
    freq = freqs[idx]
    freq_in_hertz = abs(freq * RATE)
    frequency_data.append(freq_in_hertz)
    print(freq_in_hertz)		# for testing
    
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()


