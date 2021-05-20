
import os

files_to_process = ["sunny_retinanet.txt", "rainy_retinanet.txt", "cloudy_retinanet.txt", "night_retinanet.txt"]

seen_classes = []
for f_name in files_to_process:

    folder_prefix = "subclasses/" + f_name.split(".txt")[0] + "/"
    os.system("cd subclasses && mkdir " + f_name.split(".txt")[0])
    file = open(f_name)

    for l in file.readlines():
        subclass = l.split('/')[2]
        if subclass not in seen_classes:
            seen_classes.append(subclass)
        subfile = open(folder_prefix + subclass + ".txt", 'a', encoding='utf-8')
        subfile.write(l)
        subfile.close()

    file.close()

f = open("classes.txt", 'w', encoding='utf-8')
for c in seen_classes:
    f.write(c + "\n")