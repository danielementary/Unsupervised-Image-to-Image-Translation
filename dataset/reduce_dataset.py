PATHS_FILENAMES = ["cloudy_list.txt", "sunny_list.txt"]

#return all the paths in the corresponding files
def retrieve_paths_list(paths_filenames):
    paths_list = []
    for paths_filename in paths_filenames:
        with open(paths_filename) as file:
            paths = file.readlines()
            paths_list.append(paths)
    return paths_list

#return the path without the filename
def split_directory(path):
    return "/".join(path.split("/")[:-1])

def save_paths(filename, paths):
    with open(filename, 'w') as file:
        for path in paths:
            file.write(path)

paths_list = retrieve_paths_list(PATHS_FILENAMES)

paths_to_keep = [[], []]
paths_to_delete = []
for paths in retrieve_paths_list(["night_list.txt", "rainy_list.txt"]):
    paths_to_keep += paths

for paths in paths_list:
    current_directory_paths = {}

    for path in paths:
        directory = split_directory(path)
        if directory not in current_directory_paths:
            current_directory_paths[directory] = []
        current_directory_paths[directory].append(path)

    for k,v in current_directory_paths.items():
        if len(v) < 200:
            if k[0] == 'c':
                paths_to_keep[0] += v
            else:
                paths_to_keep[1] += v
        else:
            for i in range(len(v)):
                if i%2 == 0:
                    if k[0] == 'c':
                        paths_to_keep[0] += v[i]
                    else:
                        paths_to_keep[1] += v[i]
                else:
                    paths_to_delete.append(v[i])

save_paths("to_keep_cloudy.txt", paths_to_keep[0])
save_paths("to_keep_sunny.txt",  paths_to_keep[1])
save_paths("to_delete.txt", paths_to_delete)
