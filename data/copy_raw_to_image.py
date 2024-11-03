"""
Copies ./raw/ images to ./image/ based on whether labels exist in ./label/
"""

import os
import shutil

def main(raw_dir, label_dir, img_dir):
    # Ensure the target folder exists
    os.makedirs(img_dir, exist_ok=True)

    # Get lists of JPEG and JSON files
    jpeg_files = {f for f in os.listdir(raw_dir) if f.endswith('.jpeg') or f.endswith('.jpg')}
    json_files = {f.replace('.json', '') for f in os.listdir(label_dir) if f.endswith('.json')}

    # Copy JPEG files that have a matching JSON file
    for jpeg_file in jpeg_files:
        base_name = os.path.splitext(jpeg_file)[0]
        if base_name in json_files:
            source_path = os.path.join(raw_dir, jpeg_file)
            target_path = os.path.join(img_dir, jpeg_file)
            shutil.copy2(source_path, target_path)
            print(f"Copied {jpeg_file} to {img_dir}")

if __name__ == "__main__":
    main("raw/camouflage_1", "label/camouflage_1", "img/camouflage_1")
