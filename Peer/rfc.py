"""
This code is created by:
Name: Aditya Bhardwaj
Unity ID: ABHARDW2
"""

__author__ = "Aditya Bhardwaj"
__version__ = "1.0.1"
__email__ = "abhardw2@ncsu.edu"
__status__ = "Production"

"""
This class is for sending and receiving data in RFC object in the code.
"""
class RFC: 
    def __init__(self, title = None, number = None, peerHostName = None, peerPortNumber = None):
        self.title = title
        self.number = number
        self.peerHostName = peerHostName
        self.peerPortNumber = peerPortNumber

    def getTitle(self):
        return self.title
    
    def setTitle(self, value):
        self.title = value

    def getPeerHostName(self):
        return self.peerHostName
    
    def setPeerHostName(self, value):
        self.peerHostName = value

    def getNumber(self):
        return self.number
    
    def setNumber(self, value):
        self.number = value
