import os
from pathlib import Path

resources_dir_text = "Resources_Path.txt"
model_dir_text = "Model_Path.txt"

with open(resources_dir_text, 'a') as writer:
    pass

with open(model_dir_text, 'a') as writer:
    pass

entry_list = []

with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())

if entry_list[0]:
    resources_dir = Path(str(entry_list[0]).replace('"', ''))
    print(f"Resources Directory: {resources_dir}")

    if not resources_dir.exists():
        os.mkdir(resources_dir)

    input_dir = resources_dir / "Input"
    if not input_dir.exists():
        os.mkdir(input_dir)

    output_dir = resources_dir / "Output"
    if not output_dir.exists():
        os.mkdir(output_dir)
