"""Converts a textfile w/ list of class names to global class index mapping"""

import json

def main(dir_name, f_name):
    with open(f"{dir_name}/{f_name}", "r") as f:
        labels = f.read().splitlines()

    label_to_value = {}
    current_idx = 0
    for label in labels:
        if label == '__ignore__':
            label_to_value[label] = -1
        else:
            label_to_value[label] = current_idx
            current_idx += 1

    with open(f"{dir_name}/mapping.json", "w") as f:
        json.dump(label_to_value, f, indent=4)

if __name__ == "__main__":
    main("camouflage_1", "labels.txt")
