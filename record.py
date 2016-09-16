import pyaudio
import wave
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft
from pylab import*

#CHUNK = 1024
CHUNK = 64
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



for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#for i in range(1):
    data = stream.read(CHUNK)
    frames.append(data)
    
print("* done recording")
file.write(data)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

fs, input_data = wavfile.read('output.wav')
data = input_data.T[0]
print(data)
raw_data = [(ele/2**8.)*2-1 for ele in data]
raw_transform = fft(raw_data)
freqs = fftfreq(len(raw_transform))
print(freqs.min(), freqs.max())

idx = np.argmax(np.abs(raw_transform))
print(freqs)
freq = freqs[idx]
freq_in_hertz = abs(freq * RATE)
print(freq_in_hertz)
##fs, data = wavfile.read('output.wav')
##a = data.T[0]
##b = [(ele/2**8.)*2-1 for ele in a]
##c = fft(b)
##d = len(c)/2
##plt.plot(abs(c[:(d-1)]), 'r')
##plt.show()
