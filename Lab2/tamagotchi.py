import random

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 100
        self.thirst = 100
        self.happiness = 100

    def feed(self):
        self.hunger += 20
        if self.hunger > 100:
            self.hunger = 100

    def give_water(self):
        self.thirst += 20
        if self.thirst > 100:
            self.thirst = 100

    def play(self):
        self.happiness += 20
        if self.happiness > 100:
            self.happiness = 100

    def decrease_stats(self):
        self.hunger -= random.randint(5, 15)
        self.thirst -= random.randint(5, 15)
        self.happiness -= random.randint(5, 15)

    def is_alive(self):
        return self.hunger > 0 and self.thirst > 0 and self.happiness > 0