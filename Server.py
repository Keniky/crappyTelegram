import socket
from View import GUI as UserInterface
import pickle
import threading
import sys

port = 42070

class Server:
    listOfClients = []

    def __init__(self):
        #thread
        self.serverSocket = socket.socket()
        self.serverSocket.bind(("" , port))
        self.serverSocket.listen(5)
        self.initialize() 
        #sema waits
        #sema signal
    
    def initialize(self):
        while True:
            clientSocket,self.address = self.serverSocket.accept()
            self.listOfClients.append(clientSocket)
            t = threading.Thread(target=self.receiveMessages , args=(clientSocket,)).start()
            print("connection with client established")

    def terminate(self):
        self.serverSocket.close()
        sys.exit(1)

    def receiveMessages(self , clientSocket):
        #thread recieve message
        while True:
            msg = clientSocket.recv(1024).decode()
            print(msg)
            if msg == "terminate":
                clientSocket.close()
                self.listOfClients.remove(clientSocket)
                if len(self.listOfClients) == 0:
                    self.terminate()
                break
            else:
                self.sendMessage(message=msg , clientSocket=clientSocket)
             
    def sendMessage(self , message , clientSocket):
        for s in self.listOfClients:
            if s != clientSocket:
                
                s.send(message.encode())
                

if __name__ == "__main__":
    server =Server()