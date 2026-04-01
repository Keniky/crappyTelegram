import tkinter as tk
from Controller import Client as CL
import pickle

class GUI:
    chatHeight = 23
    chatWidth = 100
    textingWidth = 70
    def __init__(self ):
        
        self.name = "Unkown"
        
        self.client = CL.Client(self)

        self.mainWindow = tk.Tk(screenName="Messanger" ,className="Messanger")
        self.mainWindow.title("Messanger")
        self.mainWindow.geometry("600x400")
        self.mainWindow.configure(background="gray")
        #self.mainWindow.bind("<KeyPress>" , self.keyListener)
        self.mainWindow.bind("<Escape>" , self.terminate)
        self.mainWindow.bind("<Return>" , self.sendMessage)
        self.mainWindow.configure(background="gray")

        #10 times better just add a menu lol
        menu = tk.Menu(self.mainWindow)
        self.mainWindow.config(menu=menu)

        connectMenu = tk.Menu(menu)
        menu.add_cascade(label="Connect" , menu=connectMenu)
        connectMenu.add_command(label="Try To Connect To Another Device" , command=self.createRequestWindow)
        connectMenu.add_separator()
        connectMenu.add_command(label="Exit" , command=self.mainWindow.destroy)

        #text area
        self.text = tk.Text(self.mainWindow , height=self.chatHeight , width=self.chatWidth)
        self.text.configure(background="gray")
        self.text.pack()
        self.text.tag_configure("right_align", justify="right")
        self.text.tag_configure("left_align", justify="left")
        self.desactivateText() 
        

        #send message area
        self.messageArea = tk.Entry(self.mainWindow , width=self.textingWidth)
        self.messageArea.pack()

        #enter ip address
        #tk.Label(self.mainWindow , text="ipAddress").grid(row=0 , column=0)
        
        #entering ip address
        #entry1.grid(row=0, column=1)

        #better way add a list of ip addresses
       # listOfIpAddresses = tk.Listbox(self.mainWindow)
       # listOfIpAddresses.insert(1,"Kali")
       # listOfIpAddresses.pack()
       # #adding button
       # tk.Button(self.mainWindow , text="Request Connection" , width=25 , command=self.connectionRequest ).pack()

    #load window
    def display(self):
        self.mainWindow.mainloop()
    #code to edit chat from controller
    def desactivateText(self):
        self.text.config(state=tk.DISABLED)
    def activateText(self):
        self.text.config(state=tk.NORMAL)
    #get text to edit it from controller
    def getText(self):
        return self.text

    #connection menu code
    def createRequestWindow(self):
        self.connectWindow = tk.Toplevel(self.mainWindow)
        
        
        tk.Label(self.connectWindow , text="ipAddress").grid(row=0 , column=0)
        ipAddressEntry = tk.Entry(self.connectWindow)
        ipAddressEntry.grid(row=0, column=1)

        tk.Label(self.connectWindow , text="Your Name").grid(row=1 , column=0)
        self.nameEntry = tk.Entry(self.connectWindow)
        self.nameEntry.grid(row=1, column=1)
        
        connectButton = tk.Button(self.connectWindow , text="Request Connection" , width= 25 , command=lambda: self.connect(ipAddressEntry.get()))
        connectButton.grid(row=2 , column=1 , padx=100 , pady= 0)
        self.connectWindow.mainloop()

#connect to machine for chatting
    def connect(self , ipAddress):
        self.client.connectToServer(ipAddress=ipAddress)
        self.name = self.nameEntry.get()
        self.connectWindow.destroy()
        
#button areay
    def sendMessage(self,event):
        msg = self.messageArea.get()
        self.writeMyMessage(msg) 
        self.client.sendMessage(msg)
#key detector
#escape to terminate 
    def terminate(self , event = None):
        self.client.terminate()
        self.mainWindow.destroy()

#message manipulation area
    def writeOtherMessage(self,msg):
        self.activateText()
        self.text.insert("end", msg + "\n", "left_align")
        self.desactivateText()
    
    def writeMyMessage(self,msg):
        self.activateText()
        self.text.insert("end", msg + "\n", "right_align")
        self.messageArea.delete(0,tk.END)
        self.desactivateText()
        