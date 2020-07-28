#!/usr/bin/env python3
import socket
import time
import sys
from datetime import timedelta

min_port = 1
max_port = 65535

#Get host
host = input("[+] Enter host name/IP: \n")

#Get IP from hostname
#If an IP is entered, it doesn't change
host = socket.gethostbyname(host)

print("\n" + "-" * 5 + " Scanning " + host + " " + "-" * 5 + "\n")

#Start timer
start = time.monotonic()

try:
    for port in range(min_port, max_port):

        #Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Get result of connection
        res = s.connect_ex((host, port))

        #Success = open
        if res == 0:
            print("Port [" + str(port) + "]:     Open")

        #Close connection before opening new connection on next port
        s.close()

#Error handling
except KeyboardInterrupt:
     print("\nCtrl+C pressed, exiting ..")
     sys.exit()
except socket.gaierror:
    print("\nHostname unresolved, exiting ..")
    sys.exit()
except socket.error:
    print("\nCouldn't connect to server, exiting ..")
    sys.exit()     

print("[+] Scan on " + host + " Complete\n")

#Elapsed time
end = time.monotonic()
elapsed = end - start
print("Ports 1-65535 scanned in: " + str(timedelta(seconds=end-start)))
