import serial
import time
import re

serial_port = 'COM3'
baud_rate = 9600
output_file = "C:\\Users\\Raghul727\\Downloads\\AirFilter2\\data\\sensor_data.txt"

ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  

with open(output_file, 'a') as file:
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(line) 

        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if numbers:
            cleaned_numbers = ' '.join(numbers).replace(" 135", "").strip()
            
            if cleaned_numbers:
                file.write(cleaned_numbers + '\n')
                file.flush()  
