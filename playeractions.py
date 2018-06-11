deck = []

suits = ["a", "b", "c", "d"]

for i in range(1,14):
	for j in suits:
		card = str(i)+j
		deck.append(card)
for i in range(4):
	deck.append("0J")
	deck.append("0w")
print deck

