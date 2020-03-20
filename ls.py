import socket
import sys
import select
import threading

# main
if __name__ == "__main__":
    LS = threading.Thread(name='LSserver')
    LS.start()

# need to make sure that the port number is given as an argument
if len(sys.argv) != 6:
    print("[LS]: ERROR: Need to include the correct number of arugments: "
          + "python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort")
    exit()

# check to make sure that the port numbers given are integer numbers
try:
    lsPortNum = int(sys.argv[1])
    ts1PortNum = int(sys.argv[3])
    ts2PortNum = int(sys.argv[5])
except Exception as err:
    print("[LS]: Please make sure to enter positive Integers greater than 1023 for the port numbers.\n")
    exit()

# make sure the port numbers given are greater than 1023
if lsPortNum <= 1023 or ts1PortNum <= 1023 or ts2PortNum <= 1023:
    print("[LS]: Please make sure the port numbers are all greater than 1023.\n")
    exit()


# this function is used to connect to the TS servers and receive any messages
def connectToTSServers(URL, TS1HostName, TS1PortNum , TS2HostName, TS2PortNum):
    # make the sockets
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Sockets created to connect to TS1 and TS2 server.")
    except socket.error as err:
        print('[LS]: Error in creating sockets: {} \n'.format(err))
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

    # send URL to look up
    message = URL
    ts1.send(message.encode('utf-8'))
    ts2.send(message.encode('utf-8'))
    print("[LS]: Sending host name " + message + " to both the servers for IP lookup ...\n")

    # these are the connections to the TS servers that select() can use to read info from
    inputs = [ts1, ts2]
    while inputs:
        # select will return 3 types of lists (respectively) : read_from , write_to , exceptions
        readable, writable, exceptional = select.select(inputs, [], [], 8)
        # we only care about reading from the TS sockets, so look into both sockets to get an IP
        for s in readable:
            # trying to get info from TS1
            if s is ts1:
                data = s.recv(1024)
                if data:
                    print("[LS]: TS1 has returned an IP for " + URL + " : " + data)
                    return data
                else:
                    readable.remove(s)
                    # inputs.remove(s)
                    s.close()

            # TS1 did not have the IP, so check TS2
            if s is ts2:
                data = s.recv(1024)
                if data:
                    print("[LS]: TS2 has returned an IP for " + URL + " : " + data)
                    return data
                else:
                    readable.remove(s)
                    # inputs.remove(s)
                    s.close()

        # both TS1 and TS2 did not have the IP, so after 8 seconds (timeout), these statements send back LS a "NOTHING"
        if not (readable or writable or exceptional):
            print("[LS]: The connections have timed out.\n"
                  + "Thus, both TS1 and TS2 do not have an IP for the following URL: " + URL)
            return "NOTHING"


# create the socket for the rs server
try:
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[LS]: Server socket created")
except socket.error as err:
    print('[LS]: socket open error: {}\n'.format(err))
    exit()

# bind the socket to the port to listen for clients
server_binding = ('', lsPortNum)
ls.bind(server_binding)
ls.listen(1)
host = socket.gethostname()
print("[LS]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[LS]: Server IP address is {}".format(localhost_ip))
print("\n")

# wait for client connections
while True:
    csockid, addr = ls.accept()
    print ("[LS]: Got a connection request from a client at {}".format(addr))

    data_from_client = csockid.recv(500)
    print("[LS]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

    # send the message to the TS servers
    msg = connectToTSServers(data_from_client, sys.argv[2], ts1PortNum, sys.argv[4], ts2PortNum)

    if msg == "NOTHING":
        msg = "" + data_from_client + " - " + "Error:HOST NOT FOUND"

    print("[LS]: Message from TS server: " + msg + " , now sending to client ...")
    # send message back to the client
    csockid.send(str(msg))
    print("\n")