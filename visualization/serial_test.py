import serial
from time import sleep


s_stream = serial.Serial(port="com3")

data = [ 1, 1, 1, 1, 0]

for d in data:
    s_stream.write(chr(d))
    sleep(2.0)



