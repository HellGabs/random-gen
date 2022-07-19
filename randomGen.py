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
import json

############# GLOBAL VARIABLES ##############
bodies = []
eyeglasses = []
hats = []
hands = []
coins = []
backgrounds = []
traits_collection = {'Body': bodies, 'Eyeglasses': eyeglasses, 'Hat': hats, 'Hands': hands, 'Coin': coins, 'Background': backgrounds}

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


        for body in bpy.data.collections['Body'].all_objects:
            bodies.append(body)

        for eyeglass in bpy.data.collections['Eyeglasses'].all_objects:
            eyeglasses.append(eyeglass)

        for hat in bpy.data.collections['Hat'].all_objects:
            hats.append(hat)

        for glove in bpy.data.collections['Hands'].all_objects:
            hands.append(glove)

        for bg in bpy.data.collections['Background'].all_objects:
            backgrounds.append(bg)

        for coin in bpy.data.collections['Coin'].all_objects:
            coins.append(coin)



    def clear_all():

        for collection in traits_collection:
            for trait in traits_collection[collection]:
                trait.hide_set(True)
                trait.hide_render = True

    def select_objects():
        metadata = {}
        for collection in traits_collection:
            trait = random.choice(traits_collection[collection])
            trait.hide_set(False)
            trait.hide_render = False

    def render_character(filename):
        bpy.context.scene.render.filepath = f"//PNG_characters\QSTN#{filename}.png"
        bpy.ops.render.render(write_still=True)

    def glb_export(filename):
        glb_folder = '//GLB_characters'
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path)
        if not os.path.isdir(directory+glb_folder):
            os.mkdir(directory+glb_folder)
        target_file = os.path.join(directory+glb_folder, f'QSTN#{filename}.glb')

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

    '''def generate_metadata(traits_info, filename):
        json_folder = '//metadata'
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path)


        metadata_template = {
            "description": "A Question character for QSTN",
            "image": "the image path (maybe ipfs/pinata?)",
            "name": f"QSTN#{filename}",
            "attributes": [
                {
                    "trait_type": "Body",
                    "value": ""
                },
                {
                    "trait_type": "Eyeglasses",
                    "value": ""
                },
                {
                    "trait_type": "Hat",
                    "value": ""
                },
                {
                    "trait_type": "Hands",
                    "value": ""
                },
                {
                    "trait_type": "Coin",
                    "value": ""
                },
                {
                    "trait_type": "Background",
                    "value": ""
                }
            ]
        }
        if not os.path.isdir(directory+json_folder):
            os.mkdir(directory+json_folder)

        for att in metadata_template['attributes']:
            att['value'] = traits_info[att['trait_type']]

        # formats the metadata template into json standards.
        result = json.dumps(metadata_template, indent=4)
        with open(f'{json_folder}/QSTN#{filename}.json', 'x') as f:
            f.write(result)'''


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