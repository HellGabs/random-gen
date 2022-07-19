import bpy
import os

def generateMetadata(traits_info, filename):
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
    if not os.path.isdir(directory + json_folder):
        os.mkdir(directory + json_folder)

    for att in metadata_template['attributes']:
        att['value'] = traits_info[att['trait_type']]

    # formats the metadata template into json standards.
    result = json.dumps(metadata_template, indent=4)
    with open(f'{json_folder}/QSTN#{filename}.json', 'x') as f:
        f.write(result)