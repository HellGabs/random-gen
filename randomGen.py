import bpy
import random

class RandomGen:
    bodies = []
    eyeglasses = []
    hats = []
    gloves = []
    backgrounds = []
    coins = []


    def get_items(self):
        for body in bpy.data.collections['BODIES'].all_objects:
            self.bodies.append(body)

        for eyeglass in bpy.data.collections['EYEGLASSES'].all_objects:
            self.eyeglasses.append(eyeglass)

        for hat in bpy.data.collections['HATS'].all_objects:
            self.hats.append(hat)

        for glove in bpy.data.collections['GLOVES'].all_objects:
            self.gloves.append(glove)

        for bg in bpy.data.collections['BACKGROUNDS'].all_objects:
            self.backgrounds.append(bg)

        for coin in bpy.data.collections['CoinswithFace'].all_objects:
            self.coins.append(coin)

    def clear_all(self):
        for body in self.bodies:
            body.hide_set(True)
            body.hide_render = True

        for eyeglass in self.eyeglasses:
            eyeglass.hide_set(True)
            eyeglass.hide_render = True

        for hat in self.hats:
            hat.hide_set(True)
            hat.hide_render = True

        for glove in self.gloves:
            glove.hide_set(True)
            glove.hide_render = True

        for bg in self.backgrounds:
            bg.hide_set(True)
            bg.hide_render = True

        for coin in self.coins:
            coin.hide_set(True)
            coin.hide_render = True

    def select_objects(self):
        randomBody = random.randrange(0, len(self.bodies) - 1)
        self.bodies[randomBody].hide_set(False)
        self.bodies[randomBody].hide_render = False

        randomEyeglass = random.randrange(0, len(self.eyeglasses) - 1)
        self.eyeglasses[randomEyeglass].hide_set(False)
        self.eyeglasses[randomEyeglass].hide_render = False

        randomHat = random.randrange(0, len(self.hats) - 1)
        self.hats[randomHat].hide_set(False)
        self.hats[randomHat].hide_render = False

        randomGlove = random.randrange(0, len(self.gloves) - 1)
        self.gloves[randomGlove].hide_set(False)
        self.gloves[randomGlove].hide_render = False

        randomBg = random.randrange(0, len(self.backgrounds) - 1)
        self.backgrounds[randomBg].hide_set(False)
        self.backgrounds[randomBg].hide_render = False

        randomCoin = random.randrange(0, len(self.coins) - 1)
        self.coins[randomCoin].hide_set(False)
        self.coins[randomCoin].hide_render = False