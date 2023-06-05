import random

def make_deck():
    deck = {
            "2 Hearts": 2, "3 Hearts": 3, "4 Hearts": 4, "5 Hearts": 5, "6 Hearts": 6, "7 Hearts": 7, "8 Hearts": 8, "9 Hearts": 9, "J Hearts": 10, "Q Hearts": 10, "K Hearts": 10, "A Hearts": 11,
            "2 Spades": 2, "3 Spades": 3, "4 Spades": 4, "5 Spades": 5, "6 Spades": 6, "7 Spades": 7, "8 Spades": 8, "9 Spades": 9, "J Spades": 10, "Q Spades": 10, "K Spades": 10, "A Spades": 11,
            "2 Diamond": 2, "3 Diamond": 3, "4 Diamond": 4, "5 Diamond": 5, "6 Diamond": 6, "7 Diamond": 7, "8 Diamond": 8, "9 Diamond": 9, "J Diamond": 10, "Q Diamond": 10, "K Diamond": 10, "A Diamond": 11,
            "2 Clubs": 2, "3 Clubs": 3, "4 Clubs": 4, "5 Clubs": 5, "6 Clubs": 6, "7 Clubs": 7, "8 Clubs": 8, "9 Clubs": 9, "J Clubs": 10, "Q Clubs": 10, "K Clubs": 10, "A Clubs": 11
            }
    return deck

def get_random(deck) -> (str, int):
    rand = random.randint(1, 54)
    count = 0
    for key, value in deck.items():
        if count == rand:
            (k, v) = (key, value)
            deck.pop(key)
            return (k, v)
        else:
            count += 1

    print("issue finding random card")
    return ("2 Hearts", 2)
