#!/usr/bin/env python3
import socket
import time
import threading
import sys
from queue import Queue
from datetime import timedelta

socket.setdefaulttimeout(0.5)

# Port range
minPort = 1
maxPort = 65535

# Prevents multi threading from incorrectly interfering with vars
print_lock = threading.Lock()

# Get hostname/IP
host = input("[+] Enter host name/IP: \n")

# Converts hostname to IP (if not already given)
host = socket.gethostbyname(host)

print("\n" + "-" * 5 + " Scanning " + host + " " + "-" * 5 + "\n")

# Start timer
start = time.monotonic()


# Define Port Scan process
def sockScan(port):
    # create socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try connection
    try:
        # Open connection
        req = s.connect((host, port))

        # Get potential service (based on /etc/services)
        try:
            service = socket.getservbyport(port)
        except Exception as e:
            service = "Unknown"
        # Print lock
        with print_lock:
            print(str(port) + ' is open --> Maybe: ' + service)

        # Close connection
        req.close()

    except:
        pass


# Define threading process
def threader():
    while True:
        # Get thread from queue
        thread = q.get()

        # Run job with thread
        sockScan(thread)

        # Complete thread
        q.task_done()


# Create queue
q = Queue()

for x in range(200):
    # Create each thread
    t = threading.Thread(target=threader)

    # Daemonise thread
    t.daemon = True

    # Start thread
    t.start()


# Port range for thread
for worker in range(minPort, maxPort):
    q.put(worker)

# Wait for thread to end
q.join()

# Elapsed time
end = time.monotonic()
elapsed = end - start
print("Ports 1-65535 scanned in: " + str(timedelta(seconds=end - start)))
