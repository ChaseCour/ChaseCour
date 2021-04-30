 # A server program which accepts requests from clients to capitalize strings. When
 # clients connect, a new thread is started to handle a client. The receiving of the
 # client data, the capitalizing, and the sending back of the data is handled on the
 # worker thread, allowing much greater throughput because more clients can be handled
 # concurrently.

import socketserver
import threading
import sys
import random
import time
import pickle


toSend = [0]*8
dict = {}
deck = []
unchangedDeck = []
players = []
data = ""

class Player:
    def __init__(self , name):
        self.name = name
        self.hand = []
        self.total = 0
        self.hasAce = False
class Card:
    def __init__(self, val, index):
        if (val > 9):
            self.value = 10
        else:
            self.value = val
        self.index = index
#-----------   GAME SET UP   -----------

def setUpGame():
    createDeck()
    shuffleDeck()
def createDeck():
    count = 0
    global deck
    for i in range(1,14):
        unchangedDeck.append(Card(i , count))
        count = count + 1
    for i in range(1,14):
        unchangedDeck.append(Card(i , count))
        count = count + 1
    for i in range(1,14):
        unchangedDeck.append(Card(i , count))
        count = count + 1
    for i in range(1,14):
        unchangedDeck.append(Card(i , count))
        count = count + 1
    tempDeck = unchangedDeck.copy()
    while len(tempDeck) > 0:
        deck.append(tempDeck.pop(random.randint(0,len(tempDeck) -1)))
    print("Shuffling...")
def shuffleDeck():
    global deck
    global unchangedDeck
    if len(deck) < 18:
        tempDeck = unchangedDeck.copy()
        deck.clear()
        while len(tempDeck) > 0:
            deck.append(tempDeck.pop(random.randint(0,len(tempDeck) -1)))
        print("Shuffling...")

#-----------   NEW HANDS   -----------

def newHands(player, conn):
    global toSend
    for i in players:
        i.hand = []
        i.hasAce = False
    startDeal()
    time.sleep(.5)
    data = []
    toSend[0]=0
    nameCards(player,conn)
def startDeal():
    global toSend
    toSend[3] = 2
    for i in players:
        i.hand.append(deck.pop(0))
    for i in players:
        i.hand.append(deck.pop(0))
    nameDealerCard()

#-----------   MANAGE GAME   -----------

def handleValue(playerInput, conn):
    global toSend
    value = 0
    hasAce = False
    for i in playerInput.hand:
        if i.value != 1:
            value = value + i.value
        elif i.value == 1 and playerInput.hasAce:
            value = value + 1
            playerInput.hasAce = True
        elif i.value == 1:
            value = value + 11
            playerInput.hasAce = True
    if value > 31:
        playerInput.value = -1
        toSend[1] = -1
        whoWon()
    elif value > 21 and playerInput.hasAce == True:
        value = value - 10
        toSend[1] = value
        playerInput.value = value
    elif value > 21 and playerInput.hasAce == False:
        toSend[1] = -1
        playerInput.value = -1
        dealerTotal()
        whoWon()
        sendIt(conn)
    elif value == 31 and playerInput.hasAce == True:
        toSend[1] = 21
        dealerTotal()
        whoWon()
    elif value == 21 and playerInput.hasAce == False:
        toSend[1] = 21
        dealerTotal()
        whoWon()
    else:
        toSend[1] = value
        playerInput.total = value
    sendIt(conn)
def handleInput(playerInput,input,conn):
    global toSend
    if input == "H":
        playerInput.hand.insert(0,deck.pop(0))
        toSend.insert(4,playerInput.hand[0])
        nameCards(playerInput,conn)
    elif input == "S":
        dealerTotal()
        whoWon()
        sendIt(conn)
    elif input == "Q":
        return
    elif input == "N":
        toSend = [0]*8
        newHands(playerInput,conn)
    else:
        print("Please input a proper response!")
def hasAce(playerInput):
    for i in playerInput.hand:
        if i.value == 1:
            return True
    return False

#-----------   DETERMINE WINNER   -----------

def dealerTotal():
    value = 0
    dealer = players[1]
    dealer.hasAce = False
    for i in range(4,len(toSend)):
        if toSend[i] < 0:
            toSend[i] = toSend[i] * -1
    for i in dealer.hand:
        if i.value != 1:
            value = value + i.value
        elif i.value == 1:
            value = value + 11
            dealer.hasAce = True
    if 16 < value < 22:
        dealer.value = value
        toSend[2] = dealer.value
    elif value > 31 and dealer.hasAce == True:
        dealer.value = -1
    elif value > 21 and dealer.hasAce == False:
        dealer.value = -1
        toSend[2] = -1
        return
    elif value < 17:
        temp = deck.pop(0)
        dealer.hand.append(temp)
        toSend.append(temp.index)
        dealerTotal()
        return
    elif value > 21 and dealer.hasAce == True:
        value = value - 10
        if 16 < value < 22:
            dealer.value = value
            toSend[2] = dealer.value
        elif value > 21:
            dealer.value = -1
            toSend[2] = -1
        else:
            temp = deck.pop(0)
            dealer.hand.append(temp)
            toSend.append(temp.index)
            dealerTotal()
            return
def whoWon():
    global toSend
    if toSend[1] == -1:
        toSend[0] = -1
    elif toSend[2] == toSend[1]:
        toSend[0] =  2
    elif toSend[2] < toSend[1]:
        toSend[0] =  1
    else:
        toSend[0] =  -1

#-----------   NAMING CARDS   -----------

def nameDealerCard():
    global toSend
    dealer = players[1]
    toSend[4 + toSend[3]] = dealer.hand[0].index
    toSend[4 + toSend[3] + 1] = -1 * dealer.hand[1].index
    toSend[2] = dealer.hand[0].value + dealer.hand[1].value
    if dealer.hand[0].value == 1 or dealer.hand[1].value == 1:
        toSend[2] = toSend[2] + 10
def nameCards(playerInput, conn):
    global toSend
    toSend[3] = len(playerInput.hand)
    for i in range (0,len(playerInput.hand)):
        toSend[4+i] = playerInput.hand[i].index
    handleValue(playerInput,conn)

#-----------   RUNNING SERVER   -----------
def sendIt(conn):
    global toSend
    data = pickle.dumps(toSend)
    conn.wfile.write(data)
def requestInput(conn):
    while True:
        data = conn.recv(2048)
        if not data:
            break
        data = data.decode('utf-8')
        return data


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class CapitalizeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        global toSend
        global data
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')
        setUpGame()
        dealer = Player("dealer")
        player = Player(str(client))
        players.append(player)
        players.append(dealer)
        newHands(player,self)
        data = ""
        while data != "Q":
            shuffleDeck()
            data = self.request.recv(1024).strip().decode('utf-8')
            if not data:
                break
            handleInput(player,data,self)
            time.sleep(.1)
        print(f'Closed: {client}')

with ThreadedTCPServer(('', 59896), CapitalizeHandler) as server:
    print(f'The capitalization server is running...')
    server.serve_forever()
