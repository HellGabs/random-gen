bl_info = {
    "name": "Random Gen",
    "author": "Gabriel Almeida",
    "version": (1, 0),
    "blender": (3, 0, 1),
    "location": "View3D > Sidebar > Random Gen",
    "description": "Generates random characters",
    "warning": "Check the documentation for better use",
    "wiki_url": "",
    "category": "3D View"}

import bpy
import random
from bpy.props import *
import os

############# GLOBAL VARIABLES ##############
bodies = []
eyeglasses = []
hats = []
gloves = []
backgrounds = []
coins = []


############# PROPERTIES #############
class MyProprerties(bpy.types.PropertyGroup):
    char_amount: bpy.props.IntProperty(
        name="Characters",
        description="Insert the amount of characters you want to create",
        default=1,
        min=1,
        max=4000
    )
    png_export: bpy.props.BoolProperty(
        name='Export .png',
        description='Saves a .png version of each generated character.',
        default = True
    )
    glb_export: bpy.props.BoolProperty(
        name='Export .glb',
        description='Saves a .glb version of each generated character.',
        default = False
    )



############# OPERATORS #############


class GenerateCharacters(bpy.types.Operator):
    bl_idname = 'generate.characters'
    bl_label = 'CLICK TO START'
    bl_options = {'REGISTER', 'UNDO'}

    def generate(context, amount, check_png, check_glb):
        GenerateCharacters.get_items()

        for character in range(amount):
            GenerateCharacters.clear_all()
            GenerateCharacters.select_objects()
            if check_png:
                GenerateCharacters.render_character(character + 1)
            if check_glb:
                GenerateCharacters.glb_export(character + 1)

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

    def render_character(char_number):
        bpy.context.scene.render.filepath = "//GENERATED\{}.png".format(char_number)
        bpy.ops.render.render(write_still=True)

    def glb_export(filename):
        glb_folder = '//GLB_characters'
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path)
        if not os.path.isdir(directory+glb_folder):
            os.mkdir(directory+glb_folder)
        target_file = os.path.join(directory+glb_folder, f'{filename}.glb')

        bpy.ops.export_scene.gltf(
            filepath=target_file,
            export_format='GLB',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_lights=True,
            export_cameras=True,
            use_visible=True)

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        GenerateCharacters.generate(context, mytool.char_amount, mytool.png_export, mytool.glb_export)
        return {'FINISHED'}


############# PANEL UI #############

class MainPanel(bpy.types.Panel):
    bl_category = "Random Gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Export"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.label(text="Set the amount:")
        layout.prop(mytool, "char_amount")
        layout.label(text="Render configs")
        layout.prop(mytool, "png_export")
        layout.prop(mytool, "glb_export")

        layout.label(text="Generate characters:")
        row = layout.row()
        row.operator("generate.characters")
        row.scale_y = 3.0


############# LOAD ADDON CLASSES #############

def register():
    bpy.utils.register_class(GenerateCharacters)
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(MyProprerties)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProprerties)


def unregister():
    bpy.utils.unregister_class(GenerateCharacters)
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(MyProprerties)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
