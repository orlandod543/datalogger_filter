Software written in python that implements a datalogger for a dust filter.
Collects the data from a serial port, stores it in a text file and upload them to dropbox.

It starts automatically in raspberry by means of systemd.

It uses the modules pyserial and dropbox. 
Usage:

- Copy the repository v0.02 to the raspberry.
- Make the file installer.sh executable and execute it.
