bl_info = {
    "name": "Random Gen",
    "author": "Gabriel Almeida",
    "version": (2, 0),
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
traits_collection = {'Body': bodies, 'Eyewear': eyeglasses, 'Hat': hats, 'Hands': hands, 'Coin': coins,
                     'Background': backgrounds}


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
        default=True
    )
    glb_export: bpy.props.BoolProperty(
        name='Export .glb',
        description='Saves a .glb version of each generated character.',
        default=False
    )
    char_type: bpy.props.StringProperty(
        name="Character Type",
        default="Question"
    )


############# OPERATORS #############


class GenerateCharacters(bpy.types.Operator):
    bl_idname = 'generate.characters'
    bl_label = 'CLICK TO START'
    bl_options = {'REGISTER', 'UNDO'}

    def generate(context, amount, check_png, check_glb, char_type):

        character_metadata = {}
        GenerateCharacters.get_items()

        for character in range(amount):
            GenerateCharacters.clear_all()
            character_metadata = GenerateCharacters.select_objects(char_type)
            if check_png:
                GenerateCharacters.render_character(character + 1)
                GenerateCharacters.generate_metadata(character_metadata, str(character + 1))
            if check_glb:
                GenerateCharacters.glb_export(character + 1)

    def get_items():

        for body in bpy.data.collections['Body'].all_objects:
            bodies.append(body)

        for eyeglass in bpy.data.collections['Eyewear'].all_objects:
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

    def select_objects(type):

        metadata = {'Character': type, 'Body': '', 'Eyewear': '', 'Hat': '', 'Hands': '', 'Coin': '',
                    'Background': ''}
        for collection in traits_collection:
            trait = random.choice(traits_collection[collection])
            trait.hide_set(False)
            trait.hide_render = False
            metadata[collection] = GenerateCharacters.format_string(trait.name)

        return metadata

        print(json.dumps(metadata, indent=4))

    def render_character(filename):
        bpy.context.scene.render.filepath = f"//PNG_characters\QSTN#{filename}.png"
        bpy.ops.render.render(write_still=True)

    def glb_export(filename):
        glb_folder = '//GLB_characters'
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path)
        if not os.path.isdir(directory + glb_folder):
            os.mkdir(directory + glb_folder)
        target_file = os.path.join(directory + glb_folder, f'QSTN#{filename}.glb')

        bpy.ops.export_scene.gltf(
            filepath=target_file,
            export_format='GLB',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_lights=True,
            export_cameras=True,
            use_visible=True)

    def format_string(txt):
        txt = txt.replace('-', ' ')
        txt = txt.title()
        return txt.split('.')[0]

    def generate_metadata(traits_info, filename):
        json_folder = 'metadata'
        # .blend file name
        blendfile = bpy.path.basename(bpy.context.blend_data.filepath)

        # .blend file path
        filepath = bpy.data.filepath.split(blendfile)[0]
        metadata_template = {
            "description": "A character for QSTN Collection",
            "image": "the image path (maybe ipfs/pinata?)",
            "name": f"QSTN#{filename}",
            "attributes": [
                {
                    "trait_type": "Character",
                    "value": ""
                },
                {
                    "trait_type": "Body",
                    "value": ""
                },
                {
                    "trait_type": "Eyewear",
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
        if not os.path.isdir(filepath + json_folder):
            os.mkdir(filepath + json_folder)

        for att in metadata_template['attributes']:
            att['value'] = traits_info[att['trait_type']]

        # formats the metadata template into json standards.
        result = json.dumps(metadata_template, indent=4)
        with open(f'{json_folder}/QSTN#{filename}.json', 'x') as f:
            f.write(result)

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        self.generate(context, mytool.char_amount, mytool.png_export, mytool.glb_export, mytool.char_type)
        return {'FINISHED'}


### Generates a .json file containing the rarity value of each trait.
class RarityIndex(bpy.types.Operator):
    bl_idname = 'generate.rarity'
    bl_label = 'Generate Rarity Index'
    bl_options = {'REGISTER', 'UNDO'}

    traits_collection = {'Body': [], 'Eyewear': [], 'Hat': [], 'Hands': [], 'Coin': [], 'Background': []}


    # this metadata will follow this pattern:
    # "character": [
    #   {
    #       "name": "TRAIT_NAME",
    #       "rarity": "RARITY_VALUE"
    #   },
    #   {...},
    # ]
    # I'm writing this because i know you have a shitty memory.
    # Also because you're dumb :)
    metadata_template = {
        "Character": [
            {"name": "Question", "rarity": 0.0},
            {"name": "Hashtag", "rarity": 0.0},
            {"name": "Exclamation", "rarity": 0.0},
            {"name": "Comma", "rarity": 0.0}
        ],
        "Body": [],
        "Eyewear": [],
        "Hat": [],
        "Hands": [],
        "Coin": [],
        "Background": []
    }

    def format_string(self, txt):
        txt = txt.replace('-', ' ')
        txt = txt.title()
        return txt.split('.')[0]

    def get_items(self):
        for key in self.traits_collection:
            for item in bpy.data.collections[key].all_objects:
                traits_collection[key].append(self.format_string(item.name))


    def generate(self):
        filename = 'RARITIES'
        json_folder = 'metadata'
        # .blend file name
        blendfile = bpy.path.basename(bpy.context.blend_data.filepath)
        # .blend file path
        filepath = bpy.data.filepath.split(blendfile)[0]

        self.get_items()

        for trait in traits_collection:
            for item in traits_collection[trait]:
                self.metadata_template[trait].append({"name": str(item), "rarity": 0.0})

        # checks if the metadata folder exists. If doesn't, it will create it.
        if not os.path.isdir(filepath + json_folder):
            os.mkdir(filepath + json_folder)

        # formats the metadata template into json standards and save it into the folder.
        result = json.dumps(self.metadata_template, indent=4)
        with open(f'{json_folder}/{filename}.json', 'x') as f:
            f.write(result)



    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        self.generate()
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

        layout.label(text="Character:")
        layout.prop(mytool, "char_type")
        layout.label(text="Set the amount:")
        layout.prop(mytool, "char_amount")
        layout.label(text="Render configs")
        layout.prop(mytool, "png_export")
        layout.prop(mytool, "glb_export")

        layout.label(text="Rarity Index:")
        row = layout.row()
        row.operator("generate.rarity")
        row.scale_y = 2.0

        layout.label(text="Generate characters:")
        row = layout.row()
        row.operator("generate.characters")
        row.scale_y = 3.0


############# LOAD ADDON CLASSES #############

def register():
    bpy.utils.register_class(GenerateCharacters)
    bpy.utils.register_class(RarityIndex)
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(MyProprerties)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProprerties)


def unregister():
    bpy.utils.unregister_class(GenerateCharacters)
    bpy.utils.unregister_class(RarityIndex)
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(MyProprerties)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()