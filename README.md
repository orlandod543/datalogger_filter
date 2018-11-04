Software written in python that implements a datalogger for a dust filter.
Collects the data from a serial port, stores it in a text file and upload them to dropbox.

It starts automatically in raspberry by means of systemd.

It uses the modules pyserial and dropbox.

Usage:
- Connect remotely to the raspberry PI through SSH:

  ssh pi@[ip adress]

- Copy the master branch of the repository onto the home folder:

  -> cd ~/
  -> git clone https://github.com/orlandod543/datalogger_filter.git

- Make the file installer.sh executable and run it.

  -> sudo chmod +x installer.sh
  
- Install the system:

  -> ./installer.sh
  
- Reboot

  sudo reboot

Configure:

The datalogger uses a YAML configuration file.
To change the default settings:
  - Download the parameters stored onto the datalogger;

    ->scp pi@[ip adress]:datalogger_filter/conf.yaml /your/folder/conf.yaml

  - Open the file with a text editor.
  - The parameter right below DataloggerInfo is the alias of the datalogger. Modify this name according to your needs.
  -Save the file
  -Upload the file to the raspberry PI:

    -> scp /your/folder/conf.yaml pi@[ip adress]:datalogger_filter/conf.yaml
