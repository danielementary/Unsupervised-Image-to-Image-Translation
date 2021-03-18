#split and filter the maximum amount of images according to the most restricting datasets in INIT dataset

from math import floor

#filenames of the files containing the paths for the dataset images
FILENAME_PATHS = ["cloudy_list.txt", "night_list.txt", "rainy_list.txt", "sunny_list.txt"]

#filenames for the output files containing the paths to the corresponding images
FILENAME_TRAIN = "roads_list_train.txt"
FILENAME_TEST = "roads_list_test.txt"

#ratio of 4 would mean we take 4 times for images for training than for testing, 80/20
TRAIN_DATASET_RATIO = 4

#retrieve the paths
paths_list = []
for filename_path in FILENAME_PATHS:
    with open(filename_path) as file:
        paths = file.readlines()
        paths_list.append(paths)

#find the limiting class
min_paths = len(min(paths_list, key=lambda p: len(p)))

#compute how many images of each class we should keep for every class
test_quantity  = floor(min_paths/(TRAIN_DATASET_RATIO+1))
train_quantity = TRAIN_DATASET_RATIO*test_quantity

#open files to save train and test images
with open(FILENAME_TRAIN, 'w') as train_file, open(FILENAME_TEST, 'w') as test_file:
    for path in paths_list:
        #counter to keep track if next image is a train or a test one
        c = 0
        #define range with max possible step
        for i in range(0, len(path), floor(len(path)/min_paths)):
            if c % (TRAIN_DATASET_RATIO+1) == 0:
                test_file.write(path[i])
            else:
                train_file.write(path[i])

            c += 1
