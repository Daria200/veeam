import os
from re import X
import shutil
import csv
from datetime import date


path_to_source = input("Path to the source folder: ")
path_to_replica = input("Path to the replica folder: ")
author = input("Your name: ")


def check_files_and_create_report(path_to_source, path_to_replica, author):
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
    index = ""
    if files_in_directory.count("report.csv") > 0:
        index = files_in_directory.count("report.csv")
    if f"reports/report{index}.csv" in files_in_directory:
        while f"report{index}.csv" in files_in_directory:
            index + 1

    with open(f"report{index}.csv", "w", newline="") as report:
        writer = csv.writer(report)
        writer.writerow(headers)
        for row in changed_files:
            writer.writerow(row)


check_files_and_create_report(path_to_source, path_to_replica, author)
