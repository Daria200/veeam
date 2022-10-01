import os
import shutil
import csv
from datetime import date
from distutils.dir_util import copy_tree

# TODO copy folders as well
# change the path for different OS systems
# make the code run periodically
# use os.walk
# change the test


def delete_or_create_and_create_report(path_to_source, path_to_replica, author):

    # To keep stack of the changed files and build a report later
    # The report will contain those fields : ["Date", "Author", "Action", "File name"]
    changed_files = []

    # Store content of the source and replica folders
    source_contents = []
    replica_contents = []

    for root, dirs, files in os.walk(path_to_source):
        for file in files:
            full_file_path = f"{root}/{file}"
            relative_file_path = full_file_path.replace(f"{path_to_source}/", "")
            source_contents.append(relative_file_path)

    for root, dirs, files in os.walk(path_to_replica):
        for file in files:
            full_file_path = f"{root}/{file}"
            relative_file_path = full_file_path.replace(f"{path_to_replica}/", "")
            replica_contents.append(relative_file_path)

            if relative_file_path not in source_contents:
                os.remove(full_file_path)
                print(f"File {full_file_path} was deleted in the replica folder")
                changed_files.append(
                    [date.today(), author, "deletion", relative_file_path]
                )

    for root, dirs, files in os.walk(path_to_source):
        for file in files:
            full_file_path = f"{root}/{file}"
            relative_file_path = full_file_path.replace(f"{path_to_source}/", "")
            if relative_file_path not in replica_contents:
                file_to_copy = f"{path_to_source}/{relative_file_path}"
                copy_destination = f"{path_to_replica}/{relative_file_path}"
                os.makedirs(os.path.dirname(copy_destination), exist_ok=True)
                shutil.copyfile(
                    file_to_copy,
                    copy_destination,
                )
                print(f"File {file} was copied to the replica folder")
                changed_files.append(
                    [date.today(), author, "creation", relative_file_path]
                )

    headers = ["Date", "Author", "Action", "File name"]

    files_in_directory = os.listdir(".")
    index = ""
    if files_in_directory.count("report.csv") > 0:
        index = files_in_directory.count("report.csv")
    if f"report{index}.csv" in files_in_directory:
        while f"report{index}.csv" in files_in_directory:
            index = index + 1

    with open(f"report{index}.csv", "w", newline="") as report:
        writer = csv.writer(report)
        writer.writerow(headers)
        for row in changed_files:
            writer.writerow(row)


if __name__ == "__main__":
    path_to_source = input("Path to the source folder: ")
    path_to_replica = input("Path to the replica folder: ")
    author = input("Your name: ")

    delete_or_create_and_create_report(path_to_source, path_to_replica, author)
