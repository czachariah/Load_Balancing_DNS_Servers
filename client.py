import threading
import socket
import sys
import os

# need to make sure that correct arguments are given: lsHostname, lsListenPort
if len(sys.argv) != 3:
    print("ERROR: Need to include the correct amount of arguments : python client.py lsHostName lsPortNum")
    exit()

# get the hostname for LS
lsHostName = sys.argv[1]

# get the port number to connect to the LS
lsPortNum = int(sys.argv[2])
if lsPortNum <= 1023:
    print("ERROR: Need to make sure that the port numbers are > 1023")
    exit()

# try to find a RESOLVED.txt, delete it if it exists and then make a new one to write and append to
dir_name = os.path.dirname(os.path.abspath(__file__))
resolved = os.path.join(dir_name, "RESOLVED" + "." + "txt")
if os.path.exists(resolved):
    os.remove(resolved)
f = open("RESOLVED.txt", "a+")

# main
if __name__ == "__main__":
    Client = threading.Thread(name='client')
    Client.start()


