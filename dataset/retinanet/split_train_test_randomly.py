import os
import random

folder_prefix = "train_test/" 
files_to_process = ["sunny_retinanet.txt", "rainy_retinanet.txt", "cloudy_retinanet.txt", "night_retinanet.txt"]

new_files_to_process = ["train_test/to_keep_sunny.txt", "train_test/to_keep_cloudy.txt", "train_test/rainy_list.txt", "train_test/night_list.txt"]

f_log = open(folder_prefix + "split_info.txt", 'w', encoding='utf-8')
# 1 - explore to have classes and copy in new files without the prefixes:
seen_classes = []
for f_name in files_to_process:

    file = open(f_name, 'r')
    new_file_name = folder_prefix + f_name.split(".txt")[0] + "_wt_prefix.txt"
    new_file = open(new_file_name, 'w', encoding='utf-8')
    new_files_to_process.append(new_file_name)

    for l in file.readlines():
        subclass = l.split('/')[2]
        if subclass not in seen_classes:
            seen_classes.append(subclass)
        without_prefix = "/".join(l.split('/')[2:])
        new_file.write(without_prefix)

    file.close()
    new_file.close()

# 2 - split them in two groups (in FUNIT, they have train: 119 & test: 30)

fraction_train = 0.8

seen_classes.append("cloudy")
seen_classes.append("night")
seen_classes.append("sunny")
seen_classes.append("rainy")

training_classes = []
testing_classes = []

for clas in seen_classes:
    if random.random() < fraction_train:
        f_log.write(clas + " is training\n")
        training_classes.append(clas)
    else:
        f_log.write(clas + " is testing\n")
        testing_classes.append(clas)

f_log.write("\n\n")

f_log.write("training: " + str(len(training_classes)) + "\n")
f_log.write("testing: " + str(len(testing_classes)) + "\n")

f_train = open(folder_prefix + "training_with_retinanet.txt", 'w', encoding='utf-8')
f_test = open(folder_prefix + "testing_with_retinanet.txt", 'w', encoding='utf-8')


# 3 create new files with this repartition

for f_name in new_files_to_process:
    f = open(f_name, "r")
    for l in f.readlines():
        subclass = l.split('/')[0]
        if subclass in training_classes:
            # print("processing " + subclass + " to put in train")
            f_train.write(l)
        elif subclass in testing_classes:
            # print("processing " + subclass + " to put in test")
            f_test.write(l)
        else:
            print("ERROR : unknown class")
    
    f.close()

f_train.close()
f_test.close()
f_log.close()