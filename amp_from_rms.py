import pyaudio
import struct
import math
import datetime
import serial
import time




FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100 
#RATE = 48000 
INPUT_BLOCK_TIME = 1
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
CHUNK = 1024
RECORD_SECONDS = 60

amplitude_array = []
time_array = []
#mytime = time.time()
#current_milli_time = lambda: int(round(mytime.time() * 1000))

#s_stream = serial.Serial(port="com4")

#-----------------------------------------------------------

def get_rms(block):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

#----------------------------------------------------------------

def is_beat(inst_amp, amp_array_len, amp_array, prev_time, time_array):
    avg = 0
    time_avg = 0
    for i in range(amp_array_len):
        avg += amp_array[i]
        time_avg += time_array[i]
    amp_avg = avg / amp_array_len
    time_avg = time_avg/ len(time_array)
    if inst_amp > amp_avg * 1.4:
        print("BEAT DETECTED")
        #current_time = int(round(mytime.time()))
        #current_time = current_milli_time()
        current_time = int(time.time())
        new_time_val = current_time - time_avg
        del(time_array[0])
        time_array.append(new_time_val)
        print(new_time_val)
        #s_stream.write(chr(1))
    else:
        print("\n")

#------------------------------------------------------------------

pa = pyaudio.PyAudio()                                 

stream = pa.open(format = FORMAT,                      
         channels = CHANNELS,                          
         rate = RATE,                                  
         input = True,                                 
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)   

errorcount = 0                                                  

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    try:                                                    
        #block = stream.read(INPUT_FRAMES_PER_BLOCK)
        block = stream.read(CHUNK)
    except IOError, e:                                      
        errorcount += 1                                     
        print( "(%d) Error recording: %s"%(errorcount,e) )  
        noisycount = 1                                      

    amplitude = get_rms(block)
    if i > 40:
        is_beat(amplitude, len(amplitude_array), amplitude_array, time_array[40], time_array)
        del(amplitude_array[0])
        amplitude_array.append(amplitude)
        
    elif i > 2:
        amplitude_array.append(amplitude)
        #cur_time = int(round(mytime.time()))
        #time = current_milli_time()
        cur_time = int(time.time())
        new_time_val = cur_time - prev_time
        time_array.append(new_time_val)
        time_array.append(new_time_val)
        time_array.append(new_time_val)
        time_array.append(new_time_val)
        
    else:
        amplitude_array.append(amplitude)
        prev_time = int(time.time())
        #prev_time = current_milli_time()
        
print(len(amplitude_array))

    #print amplitude
