import os
from re import X
import shutil
import csv
from datetime import date

path_to_source = "./source"
path_to_replica = "./replica"
author = "Me"

files_in_source = os.listdir(path_to_source)
files_in_replica = os.listdir(path_to_replica)

changed_files = []


for file in files_in_source:
    if file not in files_in_replica:
        shutil.copyfile(f"{path_to_source}/{file}", f"{path_to_replica}/{file}")
        print(f"File {file} was copied to the replica folder")
        changed_files.append([date.today(), author, "creation", file])

for file in files_in_replica:
    if file not in files_in_source:
        os.remove(f"{path_to_replica}/{file}")
        print(f"File {file} was deleted in the replica folder")
        changed_files.append([date.today(), author, "deletion", file])

files_in_replica = os.listdir(path_to_replica)
files_in_source = os.listdir(path_to_source)

headers = ["Date", "Author", "Action", "File name"]

files_in_directory = os.listdir(".")
index = files_in_directory.count("report.csv")
if f"report{index}.csv" in files_in_directory:
    while f"report{index}.csv" in files_in_directory:
        index + 1


with open(f"report{index}.csv", "w", newline="") as report:
    writer = csv.writer(report)
    writer.writerow(headers)
    for row in changed_files:
        writer.writerow(row)
