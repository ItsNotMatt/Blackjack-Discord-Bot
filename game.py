import random
import bot
import asyncio

class Game:
    #need to make dealer score
    #need to make it so u can hit until you are satisfied or until you go over 21
    def __init__(self, user: int, card1: (str, int), card2: (str, int)) -> None:
        self.ongoing = True
        self.card1 = card1
        self.card2 = card2

        self.score = card1[1] + card2[1]
        self.dealer_score = random.randint(4, 21)
        self.user = user
        print("Making new game for user:", self.user)
        asyncio.create_task(self.check_score())

    async def hit(self):
        self.score = self.score + random.randint(2, 12)
        print("score:", self.score)
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



