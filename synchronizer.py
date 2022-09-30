import os
import shutil

path_to_source = "./source"
path_to_replica = "./replica"

files_in_source = os.listdir(path_to_source)
files_in_replica = os.listdir(path_to_replica)

copied_files = []
deleted_files = []

for file in files_in_source:
    if file not in files_in_replica:
        shutil.copyfile(f"{path_to_source}/{file}", f"{path_to_replica}/{file}")

for file in path_to_replica:
    if file not in files_in_source:
        os.remove(f"{path_to_replica}/{file}")

files_in_replica = os.listdir(path_to_replica)
files_in_source = os.listdir(path_to_source)
print(files_in_replica)
print(path_to_source)
