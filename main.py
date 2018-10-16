##Software that log the data sent by a filter through serial port
#the software is split as follows:
#each time there is a new string arriving to the serial port, it
#it time stamp it, load to a txt file with the name of the current date
#and it will upload the file to dropbox
#The example string is as follows:
#-> radio = $i          Concentration = 0




import filter

#Define filter serial port parameters
port = "/dev/ttyACM1"
baudrate = 9600

#create a filter object
f = filter.air_filter(port, baudrate, timeout=10)
print f.air_filter_start()
print f.get_name()
for i in range (0,10):
    print f.get_data()

print f.filter_close()
