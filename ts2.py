import threading
import socket
import sys

# main
if __name__ == "__main__":
    TS2 = threading.Thread(name='TS2server')
    TS2.start()

# need to make sure that the port number is given as an argument
if len(sys.argv) != 2:
    print("[TS2]: ERROR: Need to include a listen port argument.")
    exit()

TS1PortNum = int(sys.argv[1])
if TS1PortNum <= 1023:
    print("[TS2]:ERROR: Need to make sure that the port numbers are > 1023")
    exit()


# function used to insert words into the data table
def insertIntoTable(count,word,table):
    for i in range(count):
        for j in range(3):
            if table[i][j] == ".":
                table[i][j] = word
                return


# store the URLs and IPs from PROJ2-DNSTS2.txt
DNSTable = []
count = 0

# get the number of lines in the DNS list
try:
    file = open("PROJ2-DNSTS2.txt", "r")
    for line in file:
        count = count + 1
except IOError:
    print("[TS2]: ERROR opening file: PROJ2-DNSTS2.txt")
    exit()

# create the table and initialize it
for i in range(count):
    DNSTable.append([])
    for j in range(3):
        DNSTable[i].append(".")

# separate the lines into words and store each word into a list
dataList = list()
try:
   file = open("PROJ2-DNSTS2.txt","r")
   for line in file:
       for word in line.replace("\r", "").replace("\n", "").split():
           dataList.append(word)

except IOError:
    print("[TS2]: ERROR opening file: PROJ2-DNSTS2.txt")
    exit()
file.close()

# populate DNS Table with the list of words
for word in dataList:
    insertIntoTable(count, word, DNSTable)


# create the socket for the rs server
try:
    ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TS2]: Server socket created")
except socket.error as err:
    print('[TS2]: socket open error: {}\n'.format(err))
    exit()


# bind the socket to the port to listen for the client
server_binding = ('', int(sys.argv[1]))
ts2.bind(server_binding)
ts2.listen(1)
host = socket.gethostname()
print("[TS2]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[TS2]: Server IP address is {}".format(localhost_ip))
print("\n")

# get list of host names to check for
while True:
    csockid, addr = ts2.accept()
    print ("[TS2]: Got a connection request from a client at {}".format(addr))

    data_from_client = csockid.recv(500)
    print("[TS2]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

    # look through the table and see if the RS server has the IP address for the host name
    for word in range(count):
        hostToCheck = DNSTable[word][0].lower()
        if data_from_client == hostToCheck:
            msg = DNSTable[word][0] + " " + DNSTable[word][1] + " " + DNSTable[word][2]
            print("[TS1]; IP found: " + msg + "\n")
            print("Now sending back to LS")
            csockid.send(msg.encode('utf-8'))
    print("\n")