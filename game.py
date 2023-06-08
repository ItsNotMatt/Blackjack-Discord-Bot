import bot
import asyncio
import deck
import player


def find_current(id: int, games: []):
    for g in games:
            if id in g.players:
                return g
    return None 

def del_current(id: int, games: []):
    for i, g in enumerate(games):
        if id in g.players:
            games.pop(i)
            return

class Game:
    def __init__(self, players: [int]) -> None:
        self.round = Round(players[0], self)
        self.players =  list(players)
        self.player = player.Player(players[0]) 
        self.player.change_money(-50.0)
        self.ongoing = True

    def next_round(self):
        self.player.change_money(-50.0)
        self.round = Round(self.players[0], self)

    def earnings(self):
        print("End Condition:", self.round.end_condition)
        if self.round.end_condition == "blackjack":# soon to change by bet amount * something
            self.player.change_money(75.0)
            print("Hit BlackJack! Chips:", self.player.money)
        elif self.round.end_condition == "bust" or self.round.end_condition == "dealer_won": 
            self.player.change_money(0.0) 
        elif self.round.end_condition == "dealer_bust" or self.round.end_condition == "beat_dealer":
            self.player.change_money(100.0)
        else:
            print("Not valid win condition")

        if self.player.money <= 0:
            print("player out of money")
            asyncio.create_task(bot.end_game(self))
            self.ongoing = False


class Round:
    def __init__(self, user: int, game: Game) -> None:
        self.end_condition = ""
        self.ongoing = True
        self.game = game

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

    async def stand(self):
        await self.check_dealers_hand()
        print(f"Dealers hand: {self.dealer_score}, Your score: {self.score}")
        if self.score > self.dealer_score:
            self.end_condition = "beat_dealer"
            await self.end_round(True)
        else:
            self.end_condition = "dealer_won"
            await self.end_round(False)

    async def check_score(self):
        print("Score is:", self.score)
        if self.score > 21:
            print("you lost")
            self.end_condition = "bust"
            await self.end_round(False)
            return
        elif self.dealer_score > 21:
            self.end_condition = "dealer_bust"
            await self.end_round(True)
            return
        elif self.score == 21:
            print("you won")
            self.end_condition = "blackjack"
            await self.end_round(True)
        else:
            return

    async def check_dealers_hand(self):
        if self.dealer_score > 21:
            self.end_condition = "dealer_bust"
            await self.end_round(True)
        elif self.dealer_score <= 16:
            print("Current hand is less than 17:", self.dealer_score)
            (k, v) = deck.get_random(self.deck)
            card = (k, v)
            self.dealer_hand.append(card)
            self.dealer_score = self.dealer_score + card[1]

            if self.dealer_score > 21:
                self.end_condition = "dealer_bust"
                await self.end_round(False)

    def get_hands(self) -> str:
        res = "Your hand: "
        for s in self.player_hand:
            res += s[0]
            res += " "
        return f"{res}"

    async def end_round(self, won: bool):
        if won:
            await bot.won_round(self.game)
        else:
            await bot.lost_round(self.game)
        self.ongoing = False
        



