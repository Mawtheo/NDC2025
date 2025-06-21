import math

class Player:
    def __init__(self):
        self.x = 128
        self.y = 128
        self.is_touched = False

    def move_up(self):
        if self.y > 1:
            self.y -= 1
    def move_down(self):
        if self.y < 240:
            self.y += 1
    def move_right(self):
        if self.x < 240:
            self.x += 1
    def move_left(self):
        if self.x > 1:
            self.x -= 1
    def attack(self, skeleton_x, skeleton_y, skeletons):
        vector = (self.x - skeleton_x, self.y - skeleton_y)
        length = math.sqrt(vector[0]**2 + vector[1]**2)
        if length < 20:
            skeletons.pop()