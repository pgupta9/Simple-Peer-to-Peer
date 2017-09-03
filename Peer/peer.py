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
This class is a supplement class for Peer to set hostname and portnumber information
"""
class Peer: 
    def __init__(self, hostName = None, portNumber = None):
        self.hostName = hostName
        self.portNumber = portNumber

    def getHostName(self):
        return self.hostName
    
    def setHostName(self, value):
        self.hostName = value
    
    def getPortNumber(self):
        return self.portNumber
    
    def setPortNumber(self, value):
        self.portNumber = value
    
