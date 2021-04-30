import sys
import socket
import pickle
import time
from tkinter import *
from tkinter.ttk import *

go = False
message = ""
dict = {}
deck = []
data = ""
master = Tk()

#-----------   CREATING DECK   -----------

def createDeck():
    for i in range(1,14):
        deck.append(Card(i , "Hearts"))
        dict[len(dict)] = "Cards/"+ str(i) + "H.png"
    for i in range(1,14):
        deck.append(Card(i , "Spades"))
        dict[len(dict)] = "Cards/"+ str(i) + "S.png"
    for i in range(1,14):
        deck.append(Card(i , "Diamonds"))
        dict[len(dict)] = "Cards/"+ str(i) + "D.png"
    for i in range(1,14):
        deck.append(Card(i , "Clubs"))
        dict[len(dict)] = "Cards/"+ str(i) + "C.png"
class Card:
    def __init__(self, val, sui):
        self.value = val
        self.suit = sui
def hit():
    global go
    global message
    go = True
    message = "H"
    master.quit()
def endIt():
    global go
    global message
    go = True
    message='Q'
    master.quit()
def stand():
    global go
    global message
    go = True
    message = "S"
    master.quit()
def newH():
    global go
    global message
    go = True
    message = "N"
    master.quit()

def showImage(data):

    for label in master.grid_slaves():
       label.grid_forget()
#-----------   PLAYER LABELS   -----------

    l1 = Label(master, text = "DEALER")
    l2 = Label(master, text = "PLAYER")
    l1.grid(row = 0, column = 0, sticky = W, pady = 2)
    l2.grid(row = 0, column = len(data)-data[3], sticky = W, pady = 2)

#-----------   IMAGES   -----------

    imgP=[0]*data[3]
    imgD=[0]*(len(data)-data[3]-4)
    for i in range(0,data[3]):
        img = PhotoImage(file = dict[data[4+i]])
        imgP[i]= img.subsample(8, 8)
        Label(master, image = imgP[i]).grid(row = 1, column = (len(data)-data[3]+i))
    for i in range(0,len(data)-data[3]-4):
        if data[data[3]+4+i] < 0:
            img = PhotoImage(file = "Cards/gray_back.png")
            imgD[i]= img.subsample(8, 8)
            Label(master, image = imgD[i]).grid(row = 1, column = (i))
        else:
            img = PhotoImage(file = dict[data[data[3]+4+i]])
            imgD[i]= img.subsample(8, 8)
            Label(master, image = imgD[i]).grid(row = 1, column = (i))

#-----------   BUTTONS   -----------

    b1 = Button(master, text = "HIT", command=hit)
    b2 = Button(master, text = "STAND", command=stand)
    b3 = Button(master, text = "NEW DEAL", command=newH)
    b4 = Button(master, text = "QUIT", command=endIt)

    b1.grid(row = 1, column = len(data)-data[3]-4,sticky = S)
    b2.grid(row = 1, column = len(data)-data[3]-3,sticky = S)
    b3.grid(row = 1, column = len(data)-data[3]-2,sticky = S)
    b4.grid(row = 1, column = len(data)-data[3]-1,sticky = S)

#-----------   INFORMATION   -----------

    t1 = Label(master, text = "Press Hit to \nget a card")
    t1.grid(row = 1, column = len(data)-data[3]-4)
    t2 = Label(master, text = "Press Stand \nto see what \ndealer gets")
    t2.grid(row = 1, column = len(data)-data[3]-3)
    t3 = Label(master, text = "Press Quit \nto exit the \nprogram")
    t3.grid(row = 1, column = len(data)-data[3]-1)
    t4 = Label(master, text = "Press New Deal\nto get a new \nhand of cards")
    t4.grid(row = 1, column = len(data)-data[3]-2)


    if data[1] == -1:
        t5 = Label(master, text = "You have:\n BUST")
        t5.grid(row = 1, column = len(data)-data[3]-1,sticky = N)
    else:
        t5 = Label(master, text = "You have:\n " + str(data[1]))
        t5.grid(row = 1, column = len(data)-data[3]-1,sticky = N)
    if data[2] == -1:
        t6 = Label(master, text = "Dealer has:\n BUST")
        t6.grid(row = 1, column = len(data)-data[3]-4,sticky = N)
    elif data[len(data) - 1] < 0:
        t6 = Label(master, text = "Dealer has:\n")
        t6.grid(row = 1, column = len(data)-data[3]-4,sticky = N)
    else:
        t6 = Label(master, text = "Dealer has:\n " + str(data[2]))
        t6.grid(row = 1, column = len(data)-data[3]-4,sticky = N)


    if data[0] == 1:
        t7 = Label(master, text = "YOU WON")
        t7.grid(row = 1, column = len(data)-data[3]-3,sticky = N)
    if data[0] == -1:
        t8 = Label(master, text = "YOU LOST")
        t8.grid(row = 1, column = len(data)-data[3]-3,sticky = N)
    if data[0] == 2:
        t8 = Label(master, text = "IT'S A PUSH")
        t8.grid(row = 1, column = len(data)-data[3]-3,sticky = N)

    mainloop()



if len(sys.argv) != 2:
    print('Pass the server IP as the sole command line argument')
else:
    createDeck()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((sys.argv[1], 59896))
        while message != "Q":
            data = pickle.loads(sock.recv(1024))
            showImage(data)
            while go == False:
                time.sleep(.1)
            sock.sendall(f'{message}'.encode('utf-8'))
