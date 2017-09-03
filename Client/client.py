"""
This code is created by:
Name: Aditya Bhardwaj
Unity ID: ABHARDW2
"""

#!/usr/bin/env python

__author__ = "Aditya Bhardwaj"
__version__ = "1.0.1"
__email__ = "abhardw2@ncsu.edu"
__status__ = "Production"

import sys
import sched
import time
import socket
import threading
import platform
import pickle
import re
import random
from _thread import *
import os

sys.path.insert(0, '/Users/ADITYA/Desktop/IP_Project1/Peer/')

from peer import Peer
from rfc import RFC
from ProjectLinked import *
from p2pserver import Peer2PeerServer
from ProjectLinked import *
from ResponseMessage import ResponseMessage

osValue = None

if sys.version_info[0] == 3:
    from urllib.request import urlopen
    osValue = os.uname()
    osValue = osValue.sysname + ' ' + osValue.release
else:
    from urllib import urlopen
    osValue = os.uname()
    osValue = osValue[0]+ ' ' + osValue[2]

"""
This code is the Class for Client (Main Client) which will interact with the CI Server.
This code also interacts with the P2P Server which will always be listening for any connection from any peer connecting for packet.BaseException
"""
class Client: 
    def __init__(self, serverName):
        try:
            self.serverName = serverName
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.PORT = 7734
            self.rfcCount = 0
            self.sock.connect((self.serverName, self.PORT))
        except IOError:
            print("Server Unreachable!")
            pass
    

    # Method to download the RFC from the P2P server which is waiting on other Peer's server containing the data
    def downloadRFC(self, rfc_number, rfc_title, host, port):
        sock_p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_p2p.connect((host, port))
        print('Connected to Peer 2 Peer Server: ', host, port)
        os_version = platform.uname().system + ' ' + platform.uname().release
        requestData = ['GET', 'RFC', rfc_number, 'P2P-CI/1.0', host, os_version]
        sock_p2p.send(pickle.dumps(requestData))
        recvData = pickle.loads(sock_p2p.recv(1024))
        recvData.printMessage()
        current_path = os.getcwd()
        filename = "rfc_" + str(rfc_number) + ".txt"
        OS = platform.system()
        if OS == "Windows":  # determine rfc path for two different system
            filename = current_path + "\\rfc1\\" + filename
        else:
            filename = current_path + "/rfc1/" + filename

        with open(filename, 'w') as file:
            file.write(recvData.message)
        sock_p2p.close()

    # Method for finding the given file in the folder
    def findLocalRfcFiles(self):
        rfcs_path = os.getcwd() + "/rfc"
        rfcs_num = [num[num.find("c")+1:num.find(".")] for num in os.listdir(rfcs_path) if 'rfc' in num]
        return rfcs_num
        

upload_port_num = 65000 + random.randint(1, 500)
clientIP = "127.0.0.1"

# Main Method which will be running the code for Client connecting to the server

def main():
    global clientIP
    global upload_port_num
    try:
        # Starting the P2P Server at the Client and start a new thread for the same
        peerServer = Peer2PeerServer(upload_port_num)
        start_new_thread(peerServer.peer_connectionListener, ('Hello', 1))
        print('Started Peer 2 Peer Server at port:', peerServer.PORT)
        rfcList = list()
        client = Client('127.0.0.1')

        print("Connected to : " + client.serverName + " on Port Number: " + str(client.PORT))
        
        # Sending the Port Details to the Server
        client.sock.send(pickle.dumps(Peer('127.0.0.1', upload_port_num)))
        data = client.sock.recv(1024)
        print(data.decode('utf-8'))

        # While loop for getting then input from the User
        while True:
            option = input("Enter Input for Options (ADD/LOOKUP/LIST/GET/CLOSE): ")
            # ADD option to send the RFC information to the Server
            if option == "ADD":
                print("Add Option is selected to add the RFC to the Server.")
                rfcCount = int(input("Enter RFC's Available: "))
                for i in range(rfcCount):
                    rfc_var = RFC(input("RFC Title: "), int(input("RFC Number: ")), clientIP, upload_port_num)
                    client.sock.send(pickle.dumps(["ADD" ,"RFC", rfc_var, " P2P-CI/1.0"]))
                    server_data = pickle.loads(client.sock.recv(1024))
                    server_data.printMessage()

            # LOOKUP option to look up the RFC information from the Server
            elif option == "LOOKUP":
                print("LookUp Option is selected to find the RFC on the Server.")

                rfc_var = RFC(input("RFC Title: "), int(input("RFC Number: ")), clientIP, upload_port_num)
                client.sock.send(pickle.dumps(["LOOKUP", "RFC", rfc_var, "P2P-CI/1.0"]))
                server_data = pickle.loads(client.sock.recv(1024))
                server_data.printMessage()
            
            # LIST option to ask for List of RFC information from the Server
            elif option == "LIST":
                print("List Option is selected to find all RFC on the Server.")

                client.sock.send(pickle.dumps(["LIST", "ALL", "RFC", "P2P-CI/1.0"]))
                server_data = pickle.loads(client.sock.recv(1024))
                server_data.printMessage()
            
            # GET option to get the data of given RFC from Server and connect to the Peer P2P Server
            # This option will call download RFC 
            elif option == "GET":
                rfc_var = RFC(input("RFC Title: "), int(input("RFC Number: ")), clientIP)

                client.sock.send(pickle.dumps(["LOOKUP", "RFC", rfc_var, "P2P-CI/1.0"]))
                server_data = pickle.loads(client.sock.recv(1024))
                client.downloadRFC(server_data.message.number, server_data.message.title, server_data.message.peerHostName, server_data.message.peerPortNumber)
                print("File Downloaded!")
                break
            
            # Sending the CLOSE request to the Server for Closing the connection
            elif option == "CLOSE":
                client.sock.send(pickle.dumps(["EXIT", "Connection", Peer('127.0.0.1', upload_port_num),"P2P-CI/1.0" ]))
                recvmessage = client.sock.recv(1024)
                print(recvmessage.decode('utf-8'))
                client.sock.close()
                exit()
                break
            else:
                print("Please Enter the correct Option: (ADD/LOOKUP/LIST/GET/CLOSE)")
                continue

    except IOError:
        pass


if __name__ == "__main__":
    main()

