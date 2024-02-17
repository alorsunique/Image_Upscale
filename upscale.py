import os
from pathlib import Path

import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"
output_dir = resources_dir / "Output"

with open("Model_Path.txt", "r") as resources_text:
    model_path = Path(str(resources_text.readline()).replace('"', ''))

print(f"Resources Directory: {resources_dir}")
print(f"Model Path: {model_path}")

# Importing the model

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(
    scale=4,
    model_path=str(model_path),
    dni_weight=None,
    model=model,
    tile=400,
    tile_pad=10,
    pre_pad=0,
    half=True,
    gpu_id=0)

# Takes note of the files and the folder structure in the input folder

input_list = []
folder_input_list = []
for entry in input_dir.rglob('*'):
    if entry.is_file():
        folder_input_list.append(entry)
        input_list.append(entry.relative_to(input_dir))

# Lists all folders that should be created

folder_output_list = []
for entry in folder_input_list:
    relative_path = entry.relative_to(input_dir)
    parent_folder = relative_path.parent
    output_folder = output_dir / parent_folder
    if output_folder not in folder_output_list:
        folder_output_list.append(output_folder)

# Creates the folders in the output folder

for entry in folder_output_list:
    os.makedirs(entry, exist_ok=True)

# Takes note of all the images in the output folder

output_list = []
for entry in output_dir.rglob('*'):
    if entry.is_file():
        output_list.append(entry.relative_to(output_dir))

input_set = set(input_list)
output_set = set(output_list)
extra_set = output_set.difference(input_set)
to_upscale_set = input_set.difference(output_set)
to_upscale_list = sorted(list(to_upscale_set))

count = 0
max_count = len(to_upscale_list)

for entry in to_upscale_list:
    count += 1
    file_path = input_dir / entry
    print(f"{count}/{max_count} | Working: {file_path.name}")

    try:
        input_image = cv2.imread(str(file_path), cv2.IMREAD_UNCHANGED)
        output_image, _ = upsampler.enhance(input_image)

        output_name = output_dir / entry
        cv2.imwrite(str(output_name), output_image)

    except:
        print(f"File not an image that can be opened")
