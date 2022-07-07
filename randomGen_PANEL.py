bl_info = {
    "name": "Random Gen",
    "author": "Gabriel Almeida",
    "version": (0, 1),
    "blender": (3, 0, 1),
    "location": "View3D > Sidebar > Random Gen",
    "description": "Generates random characters",
    "warning": "Check the documentation for better use",
    "wiki_url": "",
    "category": "3D View"}

import bpy
import random
import randomGen

############# GLOBAL VARIABLES #############
bodies = []
eyeglasses = []
hats = []
gloves = []
backgrounds = []
coins = []


############# OPERATORS #############
class GenerateCharacters(bpy.types.Operator):
    bl_idname = 'generate.characters'
    bl_label = 'Generate'

    def generate(context):
        GenerateCharacters.get_items()
        GenerateCharacters.clear_all()
        GenerateCharacters.select_objects()

    def get_items():
        for body in bpy.data.collections['BODIES'].all_objects:
            bodies.append(body)

        for eyeglass in bpy.data.collections['EYEGLASSES'].all_objects:
            eyeglasses.append(eyeglass)

        for hat in bpy.data.collections['HATS'].all_objects:
            hats.append(hat)

        for glove in bpy.data.collections['GLOVES'].all_objects:
            gloves.append(glove)

        for bg in bpy.data.collections['BACKGROUNDS'].all_objects:
            backgrounds.append(bg)

        for coin in bpy.data.collections['CoinswithFace'].all_objects:
            coins.append(coin)

    def clear_all():
        for body in bodies:
            body.hide_set(True)
            body.hide_render = True

        for eyeglass in eyeglasses:
            eyeglass.hide_set(True)
            eyeglass.hide_render = True

        for hat in hats:
            hat.hide_set(True)
            hat.hide_render = True

        for glove in gloves:
            glove.hide_set(True)
            glove.hide_render = True

        for bg in backgrounds:
            bg.hide_set(True)
            bg.hide_render = True

        for coin in coins:
            coin.hide_set(True)
            coin.hide_render = True

    def select_objects():
        randomBody = random.randrange(0, len(bodies) - 1)
        bodies[randomBody].hide_set(False)
        bodies[randomBody].hide_render = False

        randomEyeglass = random.randrange(0, len(eyeglasses) - 1)
        eyeglasses[randomEyeglass].hide_set(False)
        eyeglasses[randomEyeglass].hide_render = False

        randomHat = random.randrange(0, len(hats) - 1)
        hats[randomHat].hide_set(False)
        hats[randomHat].hide_render = False

        randomGlove = random.randrange(0, len(gloves) - 1)
        gloves[randomGlove].hide_set(False)
        gloves[randomGlove].hide_render = False

        randomBg = random.randrange(0, len(backgrounds) - 1)
        backgrounds[randomBg].hide_set(False)
        backgrounds[randomBg].hide_render = False

        randomCoin = random.randrange(0, len(coins) - 1)
        coins[randomCoin].hide_set(False)
        coins[randomCoin].hide_render = False

    def execute(self, context):
        GenerateCharacters.generate(context)
        return {'FINISHED'}


############# PANEL UI #############

class MainPanel(bpy.types.Panel):
    bl_category = "Random Gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Configs"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text='Create a New Character')
        row = layout.row()
        row.operator("generate.characters")


############# LOAD ADDON CLASSES #############

def register():
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(GenerateCharacters)


def unregister():
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(GenerateCharacters)


if __name__ == "__main__":
    register()