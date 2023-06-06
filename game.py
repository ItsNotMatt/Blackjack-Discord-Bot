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
        card1 = (key, value)
        (key, value) = deck.get_random(self.deck)
        card2 = (key, value)
        self.player_hand = [card1, card2]

        (key, value) = deck.get_random(self.deck)
        dealer_card1 = (key, value)
        (key, value) = deck.get_random(self.deck)
        dealer_card2 = (key, value)
        self.dealer_hand = [dealer_card1, dealer_card2]

        self.score = card1[1] + card2[1]
        self.dealer_score = dealer_card1[1] + dealer_card2[1] 
        self.user = user
        asyncio.create_task(self.check_score())

    async def hit(self):
        (k, v) = deck.get_random(self.deck)
        card = (k, v)
        self.player_hand.append(card)
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
        await self.check_dealers_hand()
        print(f"Dealers hand: {self.dealer_score}, Your score: {self.score}")
        if self.score > self.dealer_score:
            await bot.won_game()
            self.ongoing = False 
        else:
            await bot.lost_game()
            self.ongoing = False 

    async def check_dealers_hand(self):
        if self.dealer_score > 21:
            await bot.won_game()
            self.ongoing = False
        elif self.dealer_score <= 16:
            print("Current hand is less than 17:", self.dealer_score)
            (k, v) = deck.get_random(self.deck)
            card = (k, v)
            self.dealer_hand.append(card)
            self.dealer_score = self.dealer_score + card[1]
            if self.dealer_score > 21:
                await bot.won_game()
                self.ongoing = False

    def get_hands(self) -> str:
        res = "Your hand: "
        for s in self.player_hand:
            res += s[0]
            res += ", "
        return f"{res}"
        
        



