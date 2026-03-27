import socket 
import threading

port = 42070

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
        self.clientSocket.send(msg.encode())
        self.clientSocket.close()

    def sendMessage(self, message):
        self.clientSocket.send(message.encode())

    def receiveMessages(self): 
        #thread
        while True:
            msg = self.clientSocket.recv(1024)
            msg = msg.decode()
            self.gui.writeOtherMessage(msg)
