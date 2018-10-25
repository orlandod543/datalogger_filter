import serial
import serial.tools.list_ports

comports =  serial.tools.list_ports.comports()
print comports

for comport in comports:
    print comport.device
