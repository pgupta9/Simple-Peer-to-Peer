"""
This code is created by:
Name: Aditya Bhardwaj
Unity ID: ABHARDW2
"""

__author__ = "Aditya Bhardwaj"
__version__ = "1.0.1"
__email__ = "abhardw2@ncsu.edu"
__status__ = "Production"

import datetime
import time
import platform
import os
from rfc import RFC
from ProjectLinked import *

# This is class for Response Message which would be sent to the receiver from Sender 
class ResponseMessage:
    # Initializing the constructor for the Class
    def __init__(self, messageCode, message, contentLength, lastmodified = None):
        self.messageCode = messageCode
        self.message = message
        self.version = 'P2P-CI/1.0'
        if self.messageCode == '200':
            self.statusCode = 'OK'
        elif self.messageCode == '404':
            self.statusCode = 'Not Found'
        elif self.messageCode == '404':
            self.statusCode = 'Bad Request'
        elif self.messageCode == '505':
            self.statusCode = 'P2P-CI Version Not Supported'
        self.date = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
        self.os = platform.uname().system + ' ' + platform.uname().release
        self.contentLength = contentLength
        self.contenttype = 'text/plain'
        self.lastmodified = lastmodified
    
    # Printing the Message received
    def printMessage(self):
        print(self.version, self.messageCode, self.statusCode)
        print('Date: ', self.date)
        print('OS: ', self.os)
        if self.lastmodified != None:
            print('Last Modified: ', self.lastmodified)
        print('ContentLength: ', self.contentLength)
        print('ContentType: ', self.contenttype)
        if type(self.message) is RFC:
            print('Title: %s Number: %d HostName: %s'%(self.message.title, self.message.number, self.message.peerHostName))
        elif type(self.message) is LinkedList_RFC:
            self.message.printAll()
        else:
            print('Message: ', self.message)