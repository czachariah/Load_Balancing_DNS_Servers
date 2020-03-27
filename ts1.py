import threading
import socket
import sys

# main
if __name__ == "__main__":
    TS1 = threading.Thread(name='TS1server')
    TS1.start()

# need to make sure that the port number is given as an argument
if len(sys.argv) != 2:
    print("[TS1]: ERROR: Need to include a listen port argument.")
    exit()

TS1PortNum = int(sys.argv[1])
if TS1PortNum <= 1023:
    print("[TS1]:ERROR: Need to make sure that the port numbers are > 1023")
    exit()


# function used to insert words into the data table
def insertIntoTable(count,word,table):
    for i in range(count):
        for j in range(3):
            if table[i][j] == ".":
                table[i][j] = word
                return


# store the URLs and IPs from PROJ2-DNSTS1.txt
DNSTable = []
count = 0

# get the number of lines in the DNS list
try:
    file = open("PROJ2-DNSTS1.txt", "r")
    for line in file:
        count = count + 1
except IOError:
    print("[TS1]: ERROR opening file: PROJ2-DNSTS1.txt")
    exit()

# create the table and initialize it
for i in range(count):
    DNSTable.append([])
    for j in range(3):
        DNSTable[i].append(".")

# separate the lines into words and store each word into a list
dataList = list()
try:
   file = open("PROJ2-DNSTS1.txt","r")
   for line in file:
       for word in line.replace("\r", "").replace("\n", "").split():
           dataList.append(word)

except IOError:
    print("[TS1]: ERROR opening file: PROJ2-DNSTS1.txt")
    exit()
file.close()

# populate DNS Table with the list of words
for word in dataList:
    insertIntoTable(count, word, DNSTable)


# create the socket for the rs server
try:
    ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TS1]: Server socket created")
except socket.error as err:
    print('[TS1]: socket open error: {}\n'.format(err))
    exit()


# bind the socket to the port to listen for the client
server_binding = ('', int(sys.argv[1]))
ts1.bind(server_binding)
ts1.listen(1)
host = socket.gethostname()
print("[TS1]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[TS1]: Server IP address is {}".format(localhost_ip))
print("\n")

# get list of host names to check for
while True:
    csockid, addr = ts1.accept()
    print ("[TS1]: Got a connection request from a client at {}".format(addr))

    data_from_client = csockid.recv(500)
    print("[TS1]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

    found = False
    # look through the table and see if the RS server has the IP address for the host name
    for word in range(count):
        hostToCheck = DNSTable[word][0].lower()
        if data_from_client == hostToCheck:
            found = True
            msg = DNSTable[word][0] + " " + DNSTable[word][1] + " " + DNSTable[word][2]
            print("[TS1]: IP found: " + msg + " , now sending back to LS ... ")
            csockid.send(msg.encode('utf-8'))
    if not found:
        print("[TS1]: No match for: " + data_from_client + "\n")
    else:
        print("\n")