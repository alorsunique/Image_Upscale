# Image Upscale
Upscale images using Real-ESRGAN. The project just simplifies interacting with the `RealESRGAN_x4plus.pth` upscaler.

`setup_directories.py` sets up all the necessary paths and folders. It first generates two text files, in which the paths of the model, such as `D:\model_path`, and the working folder, such as `D:\working_folder`, should be placed. Running the `setup_directories.py` will create the working folder with input and output folders.

Just place all the images that needs upscaling in the input folder and then run 'upscale.py'. The folder structure within the input folder will be copied in the output folder and the output file names will be the same with the input. All none image files will just be ignored and no copy will be generated in the output folder.

To install Real-ESRGAN, follow the instructions provided in their repository
