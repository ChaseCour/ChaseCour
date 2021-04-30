# Explaining The Code
### BJSFin.py
This is the server code for the project. It uses a TCP threaded server that was based on the Capitalize 
server from Toal. The biggest change is using Pickle to help send an array opposed to a string. Each 
section of the array indicates a number to help the client decide what information to show. The genral
format is [who won (0 if still playing), player total, dealer total, number of cards in the players hand,
index of the cards since both have the same dictonary, <-same (next given amount of spots have this), 
index for dealers cards, <-same (same until the end and negitive if we show the back of it)]. This code
I wrote and ran locally first then put it in the context of a server. Most of it is exactly how I would
code a local blackjack game.

### BJSFin.py
This is built off the same client code from Toal. It uses TKinter to show the information and uses a
grid with a lot of if statements to show what it needs. Since the array is how it accesses the information
there is a lot of varible numbers that are based around how many cards the player has. Each time we close
the master, reset it, then show the updated info until the user supplies input.

### Cards
This is just a folder where the cards are named and within the client code there is an index to get the
file name of everything in her based on the value and the suit of the card. There is all 52 cards and one
back of card png that are used.
