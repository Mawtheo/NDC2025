import math
from random import randint

class Skeleton:
    def __init__(self):
        self.x = randint(-100, 300)
        self.y = randint(-100, 300)
        self.coeff = 0.8

    def move(self, player_x, player_y, coeurs, player):
        vector = (player_x - self.x, player_y - self.y)
        length = math.sqrt(vector[0]**2 + vector[1]**2)
        if length > 8:
            self.x = round(self.x + self.coeff * (vector[0] / length), 1)
            self.y = round(self.y + self.coeff * (vector[1] / length), 1)
        else:
            if player.is_touched == False:
                if len(coeurs) > 0:
                    coeurs.pop()
                player.is_touched = True