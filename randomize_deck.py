#!/usr/bin/python3

from random import choice


def randomize_deck(clients, hand):
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
		for i in range(4):
			card = choice(deck)
			hand.append(card)
			deck.remove(card)
		hands.append(hand[:])
		hand.clear()


if __name__ == '__main__':
	clients = ['P1','P2','P3']
	hands = []

	randomize_deck(clients,hands)
	print(clients)
	print(hands)
