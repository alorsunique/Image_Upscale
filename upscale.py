import os
import time
from pathlib import Path

import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

resources_dir_text = "Resources_Path.txt"
model_dir_text = "Model_Path.txt"

entry_list = []
with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())
    reader.close()

resources_dir = Path(entry_list[0])
input_dir = resources_dir / "Input"
output_dir = resources_dir / "Output"

print(f"Resources Directory: {resources_dir}")

entry_list = []
with open(model_dir_text, 'r') as reader:
    entry_list.append(reader.read())
    reader.close()

model_dir = Path(entry_list[0])

print(f"Model Directory: {model_dir}")

# Importing the model

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(
    scale=4,
    model_path=str(model_dir),
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

time.sleep(2.5)

for entry in to_upscale_list:
    count += 1
    file_dir = input_dir / entry
    print(f"{count}/{max_count} | Working: {file_dir.name}")

    try:
        input_img = cv2.imread(str(file_dir), cv2.IMREAD_COLOR)
        output_img, _ = upsampler.enhance(input_img)

        output_name = output_dir / entry
        cv2.imwrite(str(output_name), output_img)

    except:
        print(f"File not an image that can be opened")
