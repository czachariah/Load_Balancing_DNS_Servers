import threading
import socket
import sys

# need to make sure that the port number is given as an argument
if len(sys.argv) != 6:
    print("[RS]: ERROR: Need to include the correct number of arugments: python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort")
    exit()

try:
    lsPortNum = int(sys.argv[1])
    ts1PortNum = int(sys.argv[3])
    ts2PortNum = int(sys.argv[5])
except Exception as err:
    print("Please make sure to enter positive Integers greater than 1023 for the port numbers.\n")
    exit();

if lsPortNum <= 1023 or ts1PortNum <= 1023 or ts2PortNum <= 1023:
    print("Please make sure the port numbers are all greater than 1023.\n")
    exit();

# create the socket for the rs server
try:
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[LS]: Server socket created")
except socket.error as err:
    print('[LS]: socket open error: {}\n'.format(err))
    exit()

# bind the socket to the port to listen for the client
server_binding = ('', lsPortNum)
ls.bind(server_binding)
ls.listen(1)
host = socket.gethostname()
print("[LS]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[LS]: Server IP address is {}".format(localhost_ip))

found = False
while True:
    csockid, addr = ls.accept()
    print ("[RS]: Got a connection request from a client at {}".format(addr))

    found = False
    data_from_client = csockid.recv(500)
    print("[RS]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

    msg = data_from_client
    csockid.send(msg.encode('utf-8'))

ls.close
exit()

if __name__ == "__main__":
    LS = threading.Thread(name='LSserver')
    LS.start()