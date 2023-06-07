
class Player:
    def __init__(self, id: int) -> None:
        self.name = "test"
        self.money = 500.0
        self.id = id 


    def change_money(self, amount: float):
        self.money += amount
        print("Money is now:", self.money)
