import tkinter as tk
from View import GUI as UserInterface
from Controller import Client


gui = UserInterface.GUI()

port = 42070

#server = Server.Server()



if __name__ == "__main__":
    
    gui.display()    