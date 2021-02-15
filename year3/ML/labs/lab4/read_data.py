from os import listdir
from os.path import isfile, join

parts_amount = 10
path = "./dataset/part"


def read_data():
    parts = []
    for i in range(1, parts_amount + 1):
        dir_path = path + str(i) + "/"
        messages = []
        legit = []
        files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        for file_name in files:
            with open(dir_path + file_name, 'r') as file_data:
                messages.append(file_data.read())
                if "legit" in file_name:
                    legit.append(1)
                else:
                    legit.append(0)
        parts.append([messages, legit])
    return parts
