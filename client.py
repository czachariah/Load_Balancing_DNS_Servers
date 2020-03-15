import threading
import socket
import sys
import os

# need to make sure that correct arguments are given: lsHostname, lsListenPort
if len(sys.argv) != 3:
    print("ERROR: Need to include the correct amount of arguments : python client.py lsHostName lsPortNum \n")
    exit()

# get the hostname for LS
lsHostName = sys.argv[1]

# get the port number to connect to the LS
lsPortNum = int(sys.argv[2])
if lsPortNum <= 1023:
    print("ERROR: Need to make sure that the port numbers are > 1023\n")
    exit()

# try to find a RESOLVED.txt, delete it if it exists and then make a new one to write and append to
dir_name = os.path.dirname(os.path.abspath(__file__))
resolved = os.path.join(dir_name, "RESOLVED" + "." + "txt")
if os.path.exists(resolved):
    os.remove(resolved)
f = open("RESOLVED.txt", "a+")

# get list of host names to look up
listOfHostNames = list()
try:
   file = open("PROJ2-HNS.txt","r")
   for line in file:
       line = line.replace("\r", "").replace("\n", "")
       listOfHostNames.append(line)
except IOError:
    print("ERROR opening file: PROJ2-HNS.txt")
    exit()
file.close()

for x in listOfHostNames:
    try:
        ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Socket created to connect to LS server.\n")
    except socket.error as err:
        print('Socket Open Error: {} \n'.format(err))
        exit()

    # get the host name and the port number ready to be ready to connect to the LS server
    ls_addr = socket.gethostbyname(lsHostName)

    # now connect to the LS server
    ls_server_binding = (ls_addr, lsPortNum)
    ls.connect(ls_server_binding)
    print("[C]; Connected to the LS server.\n")

    # send LS the host name to look up
    message = x.lower()
    ls.send(message.encode('utf-8'))
    print("[C]: Sending host name " + message + " to LS server for IP lookup ...\n")

    # print the data received from the LS to RESOLVED.txt
    data_from_server = ls.recv(500)
    print("[C]: Data received from LS server: {}".format(data_from_server.decode('utf-8')) + "\n")
    f.write(data_from_server.decode('utf-8') + "\n")

    # close the socket
    ls.close()

f.close()
exit()


# main
if __name__ == "__main__":
    Client = threading.Thread(name='client')
    Client.start()


