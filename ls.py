import threading
import socket
import sys
import select
import Queue

# need to make sure that the port number is given as an argument

if len(sys.argv) != 6:
    print("[LS]: ERROR: Need to include the correct number of arugments: python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort")
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


def connectToTSServers(URL, TS1HostName, TS1PortNum , TS2HostName, TS2PortNum):
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Sockets created to connect to TS1 and TS2 server.")
    except socket.error as err:
        print('Error in creating sockets: {} \n'.format(err))
        exit()

    # get the host name and the port number ready to be ready to connect to the TS1 and TS2 servers
    ts1_addr = socket.gethostbyname(TS1HostName)
    ts2_addr = socket.gethostbyname(TS2HostName)

    # now connect to the TS1 and TS2 servers
    ts1_server_binding = (ts1_addr, TS1PortNum)
    ts2_server_binding = (ts2_addr, TS2PortNum)
    ts1.settimeout(8)
    ts2.settimeout(8)
    ts1.connect(ts1_server_binding)
    ts2.connect(ts2_server_binding)
    print("[LS]; Connected to the TS1 and TS2 servers.\n")

    # send LS the host name to look up
    message = URL
    ts1.send(message.encode('utf-8'))
    ts2.send(message.encode('utf-8'))
    print("[LS]: Sending host name " + message + " to both the servers for IP lookup ...\n")

    try:
        msg_ts1 = ts1.recv(500)
        return msg_ts1
    except socket.timeout:
        msg_ts1 = "nothing"

    try:
        msg_ts2 = ts2.recv(500)
        return msg_ts2
    except socket.timeout:
        msg_ts2 = "nothing"

    if msg_ts1 != "nothing":
        return msg_ts1

    if msg_ts2 != "nothing":
        return msg_ts2

    return "NOTHING"


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
    print ("[LS]: Got a connection request from a client at {}".format(addr))

    data_from_client = csockid.recv(500)
    print("[LS]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

    # send the message to the TS servers
    msg = connectToTSServers(data_from_client, sys.argv[2], ts1PortNum, sys.argv[4], ts2PortNum)

    if msg == "NOTHING":
        msg = "" + data_from_client + " - " + "Error:HOST NOT FOUND"

    print("message : " + str(msg))
    # send message back to the client
    csockid.send(str(msg))

ls.close
exit()

if __name__ == "__main__":
    LS = threading.Thread(name='LSserver')
    LS.start()


'''

'''