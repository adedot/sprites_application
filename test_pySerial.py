##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed
import serial
import fcntl

serial_port = '/dev/cu.usbmodem1421'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)

with serial.Serial(serial_port, baud_rate) as ser:
    while True:
        line = ser.readline();
        line = line.decode("utf-8") #ser.readline returns a binary, convert to string
        print(line.strip(' \t\n\r'));

