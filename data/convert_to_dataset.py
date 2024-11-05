"""Synthesizes dataset from labels and images. Requires labelme."""

import os
import json
import glob
import base64
from io import BytesIO

import numpy as np
from PIL import Image

import labelme  # Conda env

def _load_img_data(json_file_path, game_dir):
    """
    Loads real images from data/img.
    
    Not currently used, as encoded image is in the label files.
    """
    image_path = os.path.join(
        f"img/{game_dir}", json_file_path.split("/")[-1].split(".")[0] + ".jpeg")
    
    with open(image_path, "rb") as f:
        image_data = np.asarray(Image.open(image_path))
    
    return image_data

def _load_img_from_json(json_file_path):
    """Reads encoded image directly from labelme's jsons."""
    # Load the Labelme JSON file
    with open(json_file_path, "r") as f:
        labelme_data = json.load(f)

    # Get the base64-encoded image data
    image_data_base64 = labelme_data.get("imageData")

    # Decode the image data
    image_data = base64.b64decode(image_data_base64)

    # Convert to an image (using PIL)
    image_data = np.asarray(Image.open(BytesIO(image_data)))

    return image_data
    

def main(game_dir: str):
    """
    :param game_dir: Directory name with game-specific labelme jsons
    """
    # Load the label mapping
    with open(f"label/{game_dir}mapping.json", "r") as f:
        label_to_value = json.load(f)

    # Paths
    out_img_dir = f"datasets/{game_dir}img/"
    out_label_dir = f"datasets/{game_dir}labels/"
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_label_dir, exist_ok=True)

    json_files = glob.glob(os.path.join("label/", game_dir, "img*.json"))

    print("Starting conversion")

    for i, json_file_path in enumerate(json_files):
        json_file_path: str = json_file_path.replace(os.sep, "/")

        print(f"{i + 1}: {json_file_path}")

        # Load the Labelme annotation
        data = labelme.LabelFile(filename=json_file_path)
        
        #  Try to load image directly from json, otherwise from file
        img = _load_img_from_json(json_file_path)
        # img = _load_img_data(json_file, game_dir)
        
        # Generate label mask using the class mapping
        lbl, _ = labelme.utils.shapes_to_label(
            img_shape=img.shape,
            shapes=data.shapes,
            label_name_to_value=label_to_value,
        )
        
        # Save the original image
        image_filename = os.path.splitext(os.path.basename(json_file_path))[0] + ".png"
        image_output_path = os.path.join(out_img_dir, image_filename)
        Image.fromarray(img).save(image_output_path)
        
        # Save the label mask
        label_filename = os.path.splitext(os.path.basename(json_file_path))[0] + "_label.png"
        label_output_path = os.path.join(out_label_dir, label_filename)
        Image.fromarray(lbl.astype(np.int32)).save(label_output_path)

if __name__ == "__main__":
    main("camouflage_1/")
