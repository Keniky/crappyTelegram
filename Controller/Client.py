import socket 
import threading

port = 42070


def crypt(text , key):
    newtext = ""

    for t in text:
       charvalue = (ord(t) + key - 65 ) % 26 

       newtext +=(chr(charvalue + 65))
    
    return newtext

def hillCrypt(text , key):
    cryptedText = ""

    if len(text) % 2 != 0:
        text += "X"

    for i in range(0 , len(text) , 2):
        for j in range(2):
            #take first letter make it in 0 26 multiply it by first row , add second letter to it same thing
            cryptedText += chr(((ord(text[i]) - 65) * key[j][0]
                                + (ord(text[i + 1]) - 65) * key[j][1] ) % 26 + 65) 

    return cryptedText 


key = "DEVEPTIVE"
length = len(key)
hillKey = [[4, 13] 
        ,[21, 18]]

class Client:
    
    def __init__(self , gui):    
        self.clientSocket = socket.socket()
        self.gui = gui

    def connectToServer(self,ipAddress):
        self.clientSocket.connect((ipAddress , port))
        self.gui.writeMyMessage("connection with server established")
        t = threading.Thread(target=self.receiveMessages).start()

    def terminate(self):
        msg = "terminate"
        msg = crypt(msg , length)
        self.clientSocket.send(msg.encode())
        self.clientSocket.close()

    def sendMessage(self, message):
        if message.startswith("/" ):
            message = message[1:]
            message = hillCrypt(message , hillKey)
        
        self.clientSocket.send(message.encode())

    def receiveMessages(self): 
        #thread
        while True:
            msg = self.clientSocket.recv(1024)
            msg = msg.decode()
            self.gui.writeOtherMessage(msg)
