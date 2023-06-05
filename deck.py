import random

deck = {
        "2 Hearts": 2, "3 Hearts": 3, "4 Hearts": 4, "5 Hearts": 5, "6 Hearts": 6, "7 Hearts": 7, "8 Hearts": 8, "9 Hearts": 9, "J Hearts": 10, "Q Hearts": 11, "K Hearts": 12, "A Hearts": 11,
        "2 Spades": 2, "3 Spades": 3, "4 Spades": 4, "5 Spades": 5, "6 Spades": 6, "7 Spades": 7, "8 Spades": 8, "9 Spades": 9, "J Spades": 10, "Q Spades": 11, "K Spades": 12, "A Spades": 11,
        "2 Diamond": 2, "3 Diamond": 3, "4 Diamond": 4, "5 Diamond": 5, "6 Diamond": 6, "7 Diamond": 7, "8 Diamond": 8, "9 Diamond": 9, "J Diamond": 10, "Q Diamond": 11, "K Diamond": 12, "A Diamond": 11,
        "2 Clubs": 2, "3 Clubs": 3, "4 Clubs": 4, "5 Clubs": 5, "6 Clubs": 6, "7 Clubs": 7, "8 Clubs": 8, "9 Clubs": 9, "J Clubs": 10, "Q Clubs": 11, "K Clubs": 12, "A Clubs": 11
        }

def get_random() -> (str, int):
    rand = random.randint(1, 54)
    count = 0
    for key, value in deck.items():
        if count == rand:
            return (key, value)
        else:
            count += 1

    print("issue finding random card")
    return ("2 Hearts", 2)
(key, value) = get_random()
card = (key, value)
print(card)
