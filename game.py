import random
import bot
import asyncio
import deck

class Game:
    #need to make dealer score
    #need to make it so u can hit until you are satisfied or until you go over 21
    def __init__(self, user: int) -> None:
        self.ongoing = True
        self.deck = deck.make_deck() 
        (key, value) = deck.get_random(self.deck)
        self.card1 = (key, value)
        (key, value) = deck.get_random(self.deck)
        self.card2 = (key, value)

        (key, value) = deck.get_random(self.deck)
        self.dealer_card1 = (key, value)
        (key, value) = deck.get_random(self.deck)
        self.dealer_card2 = (key, value)

        self.score = self.card1[1] + self.card2[1]
        self.dealer_score = self.dealer_card1[1] + self.dealer_card1[1] 
        self.user = user
        print("Making new game for user:", self.user)
        asyncio.create_task(self.check_score())

    async def hit(self):
        (k, v) = deck.get_random(self.deck)
        card = (k, v)
        self.score = self.score + card[1] 
        print(f"New card: {card[0]}\nScore:{self.score}")
        await self.check_score()

    async def check_score(self):
        print("Score is:", self.score)
        if self.score > 21:
            print("you lost")
            await bot.lost_game()
            self.ongoing = False 
            return
        elif self.dealer_score > 21:
            await bot.won_game()
            self.ongoing = False 
            return
        elif self.score == 21:
            print("you won")
            await bot.won_game()
            self.ongoing = False 
        else:
            return

    async def stand(self):
        if self.score > self.dealer_score:
            await bot.won_game()
            self.ongoing = False 
        else:
            await bot.lost_game()
            self.ongoing = False 



