# path to config from the root of FUNIT folder
path_to_config = "configs/funit_roads.yaml"

# path to the trained model from the root of FUNIT folder
path_to_model = "outputs/funit_roads/checkpoints/gen_00415000.pt"
model_iteration = 5 #this should be the third model we are testing

# all the images from which you want to translate in the trained/test_images folder at the root of FUNIT folder
inputs = {"cloudy": ["0_00006.png", "18_00132.png", "18_00992.png", "6_00001.png"],
          "night": ["0_00001.png", "2_00001.png", "2_00002.png", "2_00078.png"],
          "rainy": ["11_01004.png", "2_00585.png", "28_00067.png", "8_00164.png"],
          "sunny": ["0_00001.png", "10_00001.png", "10_00223.png", "5_00020.png"]}

# all the classes to which you want to translate in the trained/test_images folder at the root of FUNIT folder
outputs = ["cloudy", "night", "rainy", "sunny"]

def remove_file_extension(filename):
    return filename.split('.')[0]

# generate commands from all to all images
with open("translations_to_do", "w") as file:
    for k_in, v_in in inputs.items():
        for img in v_in:
            for c in outputs:
                command = "python test_k_shot.py --config {} --ckpt {} --input trained/test_images/{}/{} --class_image_folder trained/test_images/{}/ --output trained/{}/{}{}2{}.jpg\n".format(path_to_config, path_to_model, k_in, img, c, model_iteration, remove_file_extension(img), k_in, c)
                file.write(command)
