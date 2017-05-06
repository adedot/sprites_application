
import requests
import ujson as json
import serial
# Serial Information
serial_port = '/dev/cu.usbmodem1421'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)

serial_data = serial.Serial(serial_port, baud_rate)

#url to post data
url = "http://54.146.129.119:8080/blocks/"


line = serial_data.readline();
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    pixy_data = line.strip(' \t\n\r')
    if pixy_data:
        print(pixy_data)
        try:
            pixy_data # needed to get data as json object
            requests.post(url, json=json)
        except requests.exceptions.ConnectionError:
            pass
        except ValueError as msg:
            print("{}".format(msg))


