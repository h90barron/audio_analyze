import pyaudio
import wave
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft
from pylab import*

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
    print(freqs)
    freq = freqs[idx]
    freq_in_hertz = abs(freq * RATE)
    frequency_data.append(freq_in_hertz)
    print(freq_in_hertz)
    
##decoded = np.fromstring(data, dtype=np.int32)
##coef = decoded.flatten()
##print(coef)
##raw_data = [(x/2**8.)*2-1 for x in coef]
##raw_transform = fft(raw_data)
##freqs = fftfreq(len(raw_transform))
##idx = np.argmax(np.abs(raw_transform))
##print(freqs)
##freq = freqs[idx]
##freq_in_hertz = abs(freq * RATE)
##frequency_data.append(freq_in_hertz)
##print(freq_in_hertz)
    #frames.append(data)


##        audio = np.fromstring(data, dtype=np.int16)
##    audio = audio.flatten()
##    left,right = np.split(np.abs(np.fft.fft(audio)), 2)
##    y = np.add(left,right[::-1])
##    x = np.arange(CHUNK/2, dtype=float)
##    i = int((CHUNK/2)/10)
##    y = y[:i]
##    x = x[:i]*(RATE/CHUNK)
##    y = y/float(100)
d##    print(y)
print("* done recording")


stream.stop_stream()
stream.close()
p.terminate()

##for i in range(0, len(frequency_data), 10):
##    print(frequency_data[i])

##wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
##wf.setnchannels(CHANNELS)
##wf.setsampwidth(p.get_sample_size(FORMApT))
##wf.setframerate(RATE)
##wf.writeframes(b''.join(frames))
##wf.close()
##
##fs, input_data = wavfile.read('output.wav')
##data = input_data.T[0]
##raw_data = [(ele/2**8.)*2-1 for ele in data]
##raw_transform = fft(raw_data)
##freqs = fftfreq(len(raw_transform))
##print(freqs.min(), freqs.max())
##
##idx = np.argmax(np.abs(raw_transform))
##freq = freqs[idx]
##freq_in_hertz = abs(freq * RATE)
##print(freq_in_hertz)
