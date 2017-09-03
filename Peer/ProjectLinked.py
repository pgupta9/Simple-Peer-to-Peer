"""
This code is created by:
Name: Aditya Bhardwaj
Unity ID: ABHARDW2
"""

__author__ = "Aditya Bhardwaj"
__version__ = "1.0.1"
__email__ = "abhardw2@ncsu.edu"
__status__ = "Production"

# Class for Node object to be used in Linked List which would be defined later in this code
class Node: 
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext

# This class is for RFC Linked List to save all the RFC values
class LinkedList_RFC:

    def __init__(self):
        self.head = None
        self.data = None

    def isEmpty(self):
        return self.head == None
    
    # Method for adding values to the Linked List
    def add(self, value):
        self.data = Node(value)
        self.data.setNext(self.head)
        self.head = self.data
    
    # Method to get size of the Linked List
    def size(self):
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.getNext()

        return count
    
    # Method to search the RFC value based on RFC number in Linked List
    def search(self, value):
        current = self.head
        found = False
        returnValue = None
        while current != None and not found:
            if current.getData().number == value:
                found = True
                returnValue = current.getData()
            else:
                current = current.getNext()
        return returnValue
    
    # Method to remove the RFC from the Linked List on RFC Value
    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData().number == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
    
    # Method to remove remove the RFC from Linked List based on Peer Value
    def removePeer(self, host, port):
        current = self.head
        previous = None

        while current != None:
            nextNode = current.getNext()
            if current.getData().peerPortNumber == port and current.getData().peerHostName == host:
                if previous == None:
                    self.head = current.getNext()
                else:
                    previous.setNext(nextNode)
            else:
                previous = current
            current = current.getNext()

    # Method to print all the values of the Linked List 
    def printAll(self):
        cursor = self.head

        while cursor != None:
            print('RFC Number: %d | Title: %s | Host: %s | Port: %d'%(cursor.data.number, cursor.data.title, cursor.data.peerHostName, cursor.data.peerPortNumber))
            cursor = cursor.next

# This class is for Peer Linked List
class LinkedList_Peer:
    
    def __init__(self):
        self.head = None
        self.data = None

    def isEmpty(self):
        return self.head == None
    
    # Method to add values to the Linked List in Peer
    def add(self, value):
        self.data = Node(value)
        self.data.setNext(self.head)
        self.head = self.data
    
    # Method to find size of Linked List of Peer
    def size(self):
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.getNext()

        return count
    
    # Method to search for node with particular host value from Peer
    def search(self, value):
        current = self.head
        found = False
        returnValue = None
        while current != None and not found:
            if current.getData().hostName == value:
                found = True
                returnValue = current.getData()
            else:
                current = current.getNext()
        return returnValue

    # Method to find and remove a Peer from Linked List based on Port Number and Host Name
    def remove(self, host, port):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData().portNumber == port and current.getData().hostName == host:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    # Method to print all the values in the Peer Linked List
    def printAll(self):
        cursor = self.head

        while cursor != None:
            print('Host: %s and Port: %d'%(cursor.data.hostName, cursor.data.portNumber))
            cursor = cursor.next