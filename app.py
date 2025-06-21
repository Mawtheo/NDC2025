from characters import player, skeleton
import pyxel as px

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
        self.rounds = 0
        self.nb_kill = 0

        px.init(self.width, self.height, self.title, self.fps)
        # Load les ressources
        px.load("ressources.pyxres")

        # Entités
        self.player = player.Player()
        self.skeleton = skeleton.Skeleton()
        self.skeletons = []
        # Ajout d'un skeleton pour le début de partie
        self.skeletons.append(self.skeleton)

        # Temps avant de se rependre des dégats
        self.cooldown = 60

        # Emplacements des coeurs et sytème de vie
        self.coeurs = [[0, 0], [16, 0], [32, 0]]
        px.run(self.update, self.draw)


    def update(self):
        # Mouvement du joueur
        if px.btn(px.KEY_UP):
            self.player.move_up()
        if px.btn(px.KEY_DOWN):
            px.btn(px.KEY_UP)
            self.player.move_down()
        if px.btn(px.KEY_RIGHT):
            self.player.move_right()
        if px.btn(px.KEY_LEFT):
            self.player.move_left()
        # Attaque du joueur
        if px.btnp(px.KEY_SPACE):
            self.player.attack(self.skeletons[0].x, self.skeletons[0].y ,self.skeletons)
        # Compteur kill, round et ajout de skeleton
        if len(self.skeletons) == 0:
            self.nb_kill += 1
            if self.nb_kill % 5 == 0:
                self.rounds += 1
            self.skeleton = skeleton.Skeleton()
            self.skeletons.append(self.skeleton)
        else:
            # Mouvement du skeleton
            self.skeleton.move(self.player.x, self.player.y, self.coeurs, self.player)

    def gameover(self):
        # Vétification si encore en vie
        if len(self.coeurs) > 0:
            for coeur in self.coeurs:
                px.blt(coeur[0], coeur[1],0, 112, 48, 16, 16, 2)
        else:
            px.bltm(0, 0, 0, 256, 0, 256, 256)
            px.text(96, 100, "Vous etes mort", 11)
            px.text(64, 120, "Cliquer sur espace pour rejouer", 11)
            if px.btnp(px.KEY_SPACE):
                self.coeurs = [[0, 0], [16, 0], [32, 0]]
                self.rounds = 0
                self.nb_kill = 0

    def draw(self):
        # Efface l'écran
        px.cls(0)
        # Map
        px.bltm(0, 0, 0, 0, 0, 256, 256)
        # Affichage des morts
        px.blt(240, 16, 0, 96, 32, 16, 12, 2)
        px.text(232, 20, str(self.nb_kill), 14)
        # Affichage des rounds
        px.blt(240, 32, 0, 64, 32, 16, 16, 2)
        px.text(232, 36, str(self.rounds), 12)
        # Affichage du skeleton
        px.blt(self.skeleton.x, self.skeleton.y, 0, 64, 16, 16, 16, 2)
        # Affichage du joueur
        px.blt(self.player.x, self.player.y, 0, 0, 16, 16, 16, 2)

        # Victoire
        if self.rounds >= 5:
            px.bltm(0, 0, 0, 256, 0, 256, 256)
            px.text(90, 100, "Le monde est sauve !", 11)

        # Cooldown avant de pouvoir ce faire toucher
        if self.player.is_touched == True:
            if self.cooldown >= 0:
                self.cooldown -= 1
            else:
                self.cooldown = 60
                self.player.is_touched = False

        # Joueur en vie ?
        self.gameover()

if __name__ == "__main__":
    App()