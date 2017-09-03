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
import socket
import sched
import time
from _thread import *
from threading import Thread
import select
import platform
import pickle

sys.path.insert(0, '/Users/ADITYA/Desktop/IP_Project1/Peer/')

from peer import Peer
from rfc import RFC
from ResponseMessage import ResponseMessage
from ProjectLinked import *
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler

"""
This is code for Server (Centralized Index), 
"""
class Server: 
    def __init__(self):
        self.PORT = 7734
        self.HOST = '127.0.0.1' # socket.gethostname()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST,self.PORT))
        self.sock.listen(5)
        print("Server Started on Port Number: %d"%self.PORT)
        self.activePeers = LinkedList_Peer()
        self.socketList = list()
        self.rfcIndices = LinkedList_RFC()
        print("Server is Started!")

    # Method to listen to the Client and send any information asked 
    def clientListenerThread(self, client, address):
        print('Got Connection from: ', address)
        data = pickle.loads(client.recv(1024))
        host = data.hostName
        port = data.portNumber
        self.activePeers.add(Peer(data.hostName, data.portNumber))
        client.send(b"Peer information added.")
        try:
            while True:
                    data = pickle.loads(client.recv(1024))
                    print(data[0], data[1], data[2], data[3])
                    if data[0] == "ADD":
                        self.rfcIndices.add(RFC(data[2].title, data[2].number, data[2].peerHostName, data[2].peerPortNumber))
                        sendData = "Added Data into the RFC Table"
                        client.send(pickle.dumps( ResponseMessage('200', sendData, sys.getsizeof(sendData), None)))
                    elif data[0] == "LOOKUP":
                        sendData = self.rfcIndices.search(data[2].number)
                        print(sendData)
                        if not sendData:
                            sendData = "Data not found!"
                            client.send(pickle.dumps(ResponseMessage('404', sendData, sys.getsizeof(sendData), None)))
                        elif sendData:
                            client.send(pickle.dumps(ResponseMessage('200', sendData, sys.getsizeof(sendData), None)))
                    elif data[0] == "LIST":
                        sendData = self.rfcIndices
                        client.send(pickle.dumps(ResponseMessage('200', sendData, sys.getsizeof(sendData), None)))
                    elif data[0] == "EXIT":
                        self.activePeers.remove(data[2].hostName, data[2].portNumber)
                        print('Removed Peer from Peer list: ', (data[2].hostName, data[2].portNumber))
                        self.rfcIndices.removePeer(data[2].hostName, data[2].portNumber)
                        print('Removed RFCs from RFC list for: ', (data[2].hostName, data[2].portNumber))
                        client.send(b'Exiting the Central Server..')
                        break
            client.close()
        except:
            pass

# Main Method to start the server and start new thread on client listener thread for every new connection
def main():
    server = Server()
    while True:
        c, addr = server.sock.accept()
        #server.clientListenerThread(c, addr)
        start_new_thread(server.clientListenerThread, (c, addr))
    server.sock.close()
    

if __name__ == "__main__": 
    main()
