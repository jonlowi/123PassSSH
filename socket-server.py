#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from random import choice

def randomize_deck():
    print("randomize_deck")
    deck = []

    for i in range(1,len(clients)+1):
        if i == 1:
            deck.append("DA")
            deck.append("HA")
            deck.append("SA")
            deck.append("CA")
        elif i == 11:
            deck.append("DJ")
            deck.append("HJ")
            deck.append("SJ")
            deck.append("CJ")
        elif i == 12:
            deck.append("DQ")
            deck.append("HQ")
            deck.append("SQ")
            deck.append("CQ")
        elif i == 13:
            deck.append("DK")
            deck.append("HK")
            deck.append("SK")
            deck.append("CK")
        else:
            deck.append("D"+str(i))
            deck.append("H"+str(i))
            deck.append("S"+str(i))
            deck.append("C"+str(i))

    for client in clients:
        hand = []
        for j in range(4):
            card = choice(deck)
            hand.append(card)
            deck.remove(card)
        client_cards[client] = hand[:]
        hand.clear()


def accept_incoming_connections():
    print("accept_incoming_connections")
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(clients)
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        client_cards[client] = []
        Thread(target=handle_client, args=(client,)).start()

def card_distrib():
    print("card_distrib")
    randomize_deck()
    for client in client_cards:
        cards = ''
        for i in range(4):
            temp = client_cards[client][i]
            if i == 0:
                cards = cards + temp
            else:
                cards = cards + ' ' + temp
        print(clients[client]+' : '+cards)
        client.send(bytes(cards, "utf8"))


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    print("handle_client")

    name = client.recv(BUFSIZ).decode("utf8")
    print(client)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the game!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    ready = 0;

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{start}", "utf8"):
            print(name + msg.decode("utf-8"))
            for p in players:
                print("p:" + p)
                if name == p:
                    client.send(bytes("You already confirmed. Waiting for other players", "utf8"))
                    ready = 1
                    break
                else:
                    continue
            if ready == 0:
                players.append(name)
            print(players)
            if len(players) >= 3 and len(players) == len(clients):
                start_game()

            elif len(players) < 3:
                broadcast(bytes("There must be at least 3 players to start game. Currently there are " + str(len(players)), "utf8"))
            else:
                broadcast(bytes("Waiting for other players to confirm. "+ str(len(players)) +"/" + str(len(clients)) + " are confirmed", "utf8"))
        elif msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def start_game():
    print("start_game")
    broadcast(bytes("The game has started", "utf8"))
    card_distrib()

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    print("broadcast")

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
client_cards = {}
players = []
addresses = {}

HOST = ''
PORT = int(input("Enter game port: "))
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
