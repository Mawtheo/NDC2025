import pyxel as px
import math
from random import randint

""" 
Nuit du code 2025
Fait par Théo Dumez et Nathan Boucherit
"""

class App:
    def __init__(self):
        self.width = 256
        self.height = 256
        self.title = "NDC 2025"
        self.fps = 60
        self.rounds = 1
        self.nb_kill = 0
        self.nb_coins = 0

        px.init(self.width, self.height, self.title, self.fps)
        # Load des ressources
        px.load("2.pyxres")
        # Entités
        self.player = Player()
        self.skeleton = Skeleton()
        self.skeletons = []
        # Temps avant de se rependre des dégats
        self.cooldown = 60
        # Emplacements des coeurs et sytème de vie
        self.coeurs = [[0, 0], [16, 0], [32, 0]]
        px.run(self.update, self.draw)


    def update(self):
        if px.btn(px.KEY_UP):
            self.player.move_up()
        if px.btn(px.KEY_DOWN):
            px.btn(px.KEY_UP)
            self.player.move_down()
        if px.btn(px.KEY_RIGHT):
            self.player.move_right()
        if px.btn(px.KEY_LEFT):
            self.player.move_left()
        if px.btnp(px.KEY_SPACE):
            self.player.attack(self.skeletons[0].x, self.skeletons[0].y ,self.skeletons)
        if len(self.skeletons) == 0:
            self.nb_kill += 1
            if self.nb_kill % 5 == 0:
                self.rounds += 1
            self.skeleton = Skeleton()
            self.skeletons.append(self.skeleton)
        else:
            # Mouvement du skeleton
            self.skeleton.move(self.player.x, self.player.y, self.coeurs, self.player)

    def gameover(self):
        if len(self.coeurs) > 0:
            for coeur in self.coeurs:
                px.blt(coeur[0], coeur[1],0, 112, 48, 16, 16, 2)
        else:
            px.bltm(0, 0, 0, 256, 0, 256, 256)
            px.text(96, 100, "Vous etes mort", 11)
            px.text(64, 120, "Cliquez sur espace pour rejouer", 11)
            if px.btn(px.KEY_SPACE):
                self.coeurs = [[0, 0], [16, 0], [32, 0]]
                self.nb_kill = 0
                self.rounds = 1

    def draw(self):
        # Efface l'écran
        px.cls(0)
        # Map
        px.bltm(0, 0, 0, 0, 0, 256, 256)
        if len(self.skeletons) > 0:
            px.blt(self.skeleton.x, self.skeleton.y, 0, 64, 16, 16, 16, 2)
        # Affichage du joueur
        px.blt(self.player.x, self.player.y, 0, 0, 16, 16, 16, 2)
        # Affichage des pièces
        px.blt(240, 0, 0, 32, 48, 16, 16, 2)
        px.text(232, 5, str(self.nb_coins), 11)
        # Affichage des morts
        px.blt(240, 16, 0, 96, 32, 16, 12, 2)
        px.text(232, 20, str(self.nb_kill), 14)
        # Affichage des rounds
        px.blt(240, 32, 0, 64, 32, 16, 16, 2)
        px.text(232, 36, str(self.rounds), 12)
        if self.player.is_touched == True:
            if self.cooldown >= 0:
                self.cooldown -= 1
            else:
                self.cooldown = 60
                self.player.is_touched = False
        self.gameover()
        if self.rounds >= 10:
            px.bltm(0, 0, 0, 256, 0, 256, 256)
            px.text(90, 100, "Le monde est sauvé !", 11)



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



if __name__ == "__main__":
    App()