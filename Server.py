import socket
import math
from View import GUI as UserInterface
import pickle
import threading
import sys

port = 42070


hillKey = [[4, 13] 
            ,[21, 18]]
key = "DEVEPTIVE"
length = len(key)

def crypt(text , key):
    newtext = ""

    for t in text:
       charvalue = (ord(t) + key - 65 ) % 26 

       newtext +=(chr(charvalue + 65))
    
    return newtext

def deCrypt(text , key):
    newtext = ""

    for t in text:
       charvalue = (ord(t) - key - 65 ) % 26 

       newtext +=(chr(charvalue + 65))
    
    return newtext

def vigCrypt(text , key , length):
    decryptedtext = ""
    num = -1

    for i in text:
        num = (num + 1) % length

        decryptedtext += chr( ((ord(i) - 65 + ord(key[num]) )% 26) + 65)


    return decryptedtext


def vigDecrypt(text , key , length):
    decryptedtext = ""
    num = -1

    for i in text:
        num = (num + 1) % length

        decryptedtext += chr( ((ord(i) - 65 - ord(key[num]) )% 26) + 65)


    return decryptedtext


def inverseKey(key):
    inverseKey =[[0] * 2 for i in range(2)]
    det = key[0][0] * key[1][1] - key[1][0] * key[0][1] 
    det = det % 26
    if(math.gcd(26 , det) != 1):
        #print(math.gcd(26 , det))
        return None

    #in future add code to get the number instead of 15

    inverseKey[0][0] = (key[1][1] * 15 )% 26
    inverseKey[1][1] = (key[0][0] * 15 )% 26
    inverseKey[1][0] = (-key[1][0] * 15 )% 26
    inverseKey[0][1] = (-key[0][1] * 15 )% 26

    return inverseKey


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


def hillDecrypt(text , key):
    newKey = inverseKey(key)

    deCryptedText = ""


    for i in range(0 , len(text) , 2):
        for j in range(2):
            #take first letter make it in 0 26 multiply it by first row , add second letter to it same thing
            deCryptedText += chr(((ord(text[i]) - 65) * newKey[j][0]
                                + (ord(text[i + 1]) - 65) * newKey[j][1] ) % 26 + 65) 

    return deCryptedText 
 
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
            print("crypted message " + msg)
            msg = hillDecrypt(msg , hillKey)
            print("decrypted message " + msg)
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