"""
This code is created by:
Name: Aditya Bhardwaj
Unity ID: ABHARDW2
"""

__author__ = "Aditya Bhardwaj"
__version__ = "1.0.1"
__email__ = "abhardw2@ncsu.edu"
__status__ = "Production"

import socket
import pickle 
import os
import platform
import time
import sys
from ResponseMessage import ResponseMessage

"""
This file contains code for Peer 2 Peer Server which will run at the Peer side as a Server 
which will send the packet to the other client/peer asking for the file from this particular client/peer.
"""

class Peer2PeerServer:

    def __init__(self, portnumber):
        self.host = '127.0.0.1'
        self.PORT = portnumber
    
    # Code for finding the file from the given folder to send
    def findfile(self, rfcNumber):
        current_path = os.getcwd()
        filename = "rfc_" + str(rfcNumber) + ".txt"
        OS = platform.system()
        if OS == "Windows":  # determine rfc path for two different system
            filename = current_path + "\\rfc\\" + filename
        else:
            filename = current_path + "/rfc/" + filename
        if os.path.exists(filename) == False:
            sendMessage = 'File not found'
            message = ResponseMessage("404", sendMessage, sys.getsizeof(sendMessage), None)
        else:
            print(filename)
            txt = open(filename)
            sendMessage = txt.read()
            lastModified = time.ctime(os.path.getmtime(filename))
            message = ResponseMessage("200", str(sendMessage), os.path.getsize(filename), lastModified)

        return message

    # Code for this Server to listen the connection request coming from any client.
    def peer_connectionListener(self, s, i):
        self.sock = socket.socket()
        self.sock.bind((self.host, self.PORT))
        self.sock.listen(5)
        while True:
            c, addr = self.sock.accept()
            print('Got Connection from:', addr)
            data_receive = pickle.loads(c.recv(1024))
            if data_receive[0] == "GET":
                if data_receive[3] != "P2P-CI/1.0":
                    message = "Version not supported."
                else:
                    file = self.findfile(data_receive[2])
                    c.send(pickle.dumps(file))
            c.close()
