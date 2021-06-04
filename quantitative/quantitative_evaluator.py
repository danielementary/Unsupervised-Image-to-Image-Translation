from os import chdir, listdir, makedirs, system, getcwd
from os.path import exists
from random import seed, choices
from shutil import copyfile, rmtree

import sys

sys.path.insert(1, "PerceptualSimilarity")

import torch
import numpy as np

import lpips
from inception_score import inception_score

seed(0)

# location of the FUNIT repository and our dataset on the cluster
FUNIT_dir = "/ivrldata1/students/2021-spring-cs413-team3/Unsupervised-Image-to-Image-Translation/FUNIT/"
dataset_dir = "/ivrldata1/students/2021-spring-cs413-team3/INIT_dataset/"

# return the list of paths in a given file
def read_paths(filename):
    paths = []
    with open(filename, "r") as f:
        for line in f:
            # remove the \n add the end of the line
            line = dataset_dir+line[:-1]
            paths.append(line)
    
    return paths

# return n random paths from a list of paths
def gen_n_paths(paths, n):
    return choices(paths, k=n)

# create a directory to store our resutls
lpips_dir = FUNIT_dir+"scores/lpips/"
if not exists(lpips_dir):
    makedirs(lpips_dir)

source_classes = ["cloudy", "rainy", "sunny"]
target_class = "night"

# prepare paths and directories
source_images = {}
number_of_source_images = 20
number_of_pairs_per_image = 5
with open("source_paths_deblina.txt", "w") as spf:
    for c in source_classes:
        temp_paths = gen_n_paths(read_paths(c+"_train_set.txt"), number_of_source_images)
        source_images[c] = temp_paths
        spf.writelines("\n".join(temp_paths))
        spf.write("\n")
        
target_paths = read_paths(target_class+"_test_set.txt")

with open("target_paths_deblina.txt", "w") as tpf:
    for _ in range(len(source_classes)):
        for _ in range(number_of_source_images):
            temp_paths = gen_n_paths(target_paths, 2)
            tpf.writelines("\n".join(temp_paths))
            tpf.write("\n")

# locations of our pretrained FUNIT models
model_1 = "/ivrldata1/students/2021-spring-cs413-team3/models/outputs_9_with_retinanet_500K/funit_roads/checkpoints/gen_00500000.pt"
model_2 = "/ivrldata1/students/2021-spring-cs413-team3/models/outputs_balanced_483K/funit_roads/gen_00480000.pt"
model_3 = "/ivrldata1/students/2021-spring-cs413-team3/models/outputs_unbalanced_470K_1st_run/funit_roads/checkpoints/gen_00470000.pt"
model_4 = "/ivrldata1/students/2021-spring-cs413-team3/models/outputs_second_run_unbalanced_500K/funit_roads/checkpoints/gen_00500000.pt"
model_5 = "/ivrldata1/students/2021-spring-cs413-team3/models/outputs_retinanet_2_500K/funit_roads/checkpoints/gen_00500000.pt"
model_6 = "/ivrldata1/students/2021-spring-cs413-team3/models/outputs_FUNIT_finetuned_250K/funit_roads/checkpoints/gen_00250000.pt"

models = [model_1, model_2, model_3, model_4, model_5, model_6]

number_of_target_class_images = [2, 5]

# setup for lpips
loss_fn = lpips.LPIPS(net='alex')
loss_fn.cuda()

# go to the FUNIT direction to run the translation script
chdir(FUNIT_dir)

total_pairs = len(models)*len(number_of_target_class_images)*len(source_classes)*number_of_source_images*number_of_pairs_per_image
progress_counter = 0

for m in range(len(models)):
    # compare the lpips score when using multiple target class images
    for n in number_of_target_class_images:
        # directory for m'th model for n targer class images
        cwd = lpips_dir+"model_"+str(m)+"/target_"+str(n)+"/"
        if not exists(cwd):
            makedirs(cwd)
        # for each source class: cloudy, rainy and sunny
        for c in source_classes:
            class_average = 0
            imgs_is = torch.empty((2*number_of_pairs_per_image*number_of_source_images, 3, 128, 128))
            # generate number_of_pairs_per_image pairs for each of the hundred source images
            for i in range(number_of_source_images):
                image_average = 0
                for p in range(number_of_pairs_per_image):
                    progress_estimation = round(100*progress_counter/total_pairs)

                    twd = cwd+c+"2"+target_class+"/"+str(i)+"/"+str(p)+"/"
                    outputs_dir = twd + "outputs/"
                    if not exists(outputs_dir):
                        makedirs(outputs_dir)
                    
                    target_images_dir = twd + "target_images/"

                    # make sure both images were generated
                    while len(listdir(outputs_dir)) < 2:
                        # compute two translation for the given pair
                        for pp in range(2):
                            if not exists(target_images_dir):
                                makedirs(target_images_dir)
                            # copy the target images to the corresponding directory
                            target_images = gen_n_paths(target_paths, n)
                            for ti in range(n):
                                copyfile(target_images[ti], target_images_dir+"{}.png".format(ti))
                            command = "python test_k_shot.py --config configs/funit_roads.yaml --ckpt {} --input {} --class_image_folder {} --output {}.jpg".format(models[m], source_images[c][i], target_images_dir, outputs_dir+str(pp))
                            system(command + " >/dev/null 2>&1")
                            # delete target images after translation
                            rmtree(target_images_dir)

                    progress_counter += 1

                    p0 = lpips.im2tensor(lpips.load_image(outputs_dir+"0.jpg"))
                    p1 = lpips.im2tensor(lpips.load_image(outputs_dir+"1.jpg"))

                    imgs_is[i*number_of_pairs_per_image+p+0] = p0[0]
                    imgs_is[i*number_of_pairs_per_image+p+1] = p1[0]

                    p0 = p0.cuda()
                    p1 = p1.cuda()

                    d = loss_fn.forward(p0, p1).item()

                    image_average += d

                    # print("Model {}: ({}%)\n"\
                    # "with {} target images\n"\
                    # "from {} to night\n"\
                    # "{}th source image\n"\
                    # "{}th pair\n"\
                    # "-->lpips: {:.3f}\n".format(m, progress_estimation, n, c, i, p, d))

                image_average /= number_of_pairs_per_image

                # print("Model {}:\n"\
                # "with {} target images\n"\
                # "from {} to night\n"\
                # "{}th source image\n"\
                # "-->lpips {:.3f}\n".format(m, n, c, i, image_average))

                class_average += image_average

            class_average /= number_of_source_images
            is_avg, is_std = inception_score(imgs_is, resize=True)

            print("Model {}:\n"\
            "with {} target images\n"\
            "from {} to night\n"\
            "-->lpips {:.3f}\n"\
            "-->is avg {:.3f}, std {:.3f}\n".format(m, n, c, class_average, is_avg, is_std))
