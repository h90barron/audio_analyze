import pyaudio
import wave
from scipy.io import wavfile
from scipy.fftpack import fft
from pylab import*


# Attempting to filter through freq bins which will then be stored in a history
# buffer for that freq bin. The history buffer will then be used to compute the
# local energy max of that give freq range and determine if it is a beat or not in
# that range. Initially using constant audio frequency for testing. 


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

# Only one bin should contain data while using constant freq

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#for i in range(1):
    data = stream.read(CHUNK)
    decoded = np.fromstring(data, dtype=np.int32)
    coef = decoded.flatten()
    #print(coef)
    raw_data = [(x/2**8.)*2-1 for x in coef]
    raw_transform = fft(raw_data)
    #------------------------------------------------------------
    f_bin = raw_transform[:8]
    freqs = fftfreq(len(raw_transform))
    freqs = freqs[:16]
    idx = np.argmax(np.abs(f_bin))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * RATE)
    print(freq_in_hertz)
    #--------------------------------------------------------
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()




