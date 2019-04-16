IOT Monitor is a script for monitoring MAC changes to IOT devices. This script was tested on Raspberry Pi's.

The script monitors specific files and folders which are defined in the .conf file. When changes are detected, the modified, acessed
and created times are uploaded to a MySQL db residing in an amazon instance. File system information is transfered over encrypted SSH
connection. 

To Do:
-----

1. Install dependencies - fsmonitor, sshtunnel
2. Edit config file to indicate which directories and files you want to monitor
3. Edit SSH key data in the script
4. Edit MySQL connection data in the script
