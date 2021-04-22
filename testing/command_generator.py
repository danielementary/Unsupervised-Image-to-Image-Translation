# path to config from the root of FUNIT folder
path_to_config = "configs/funit_roads.yaml"

# path to the trained model from the root of FUNIT folder
path_to_model = "outputs/funit_roads/checkpoints/gen_00247500.pt"
model_iteration = 3 #this should be the third model we are testing

# all the images from which you want to translate in the trained/test_images folder at the root of FUNIT folder
inputs = {"cloudy": ["0_00006.png"],
          "night": [],
          "rainy": [],
          "sunny": []}

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
