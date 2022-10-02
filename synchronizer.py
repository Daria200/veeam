import csv
import hashlib
import os
import shutil

from datetime import date

SEP = os.sep


def check_content(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def delete_or_create_and_create_report(path_to_source, path_to_replica, author):

    # To keep stack of the changed files and build a report later
    # The report will contain those fields : ["Date", "Author", "Action", "File name"]
    changed_files = []

    # Store content of the source and replica folders
    source_contents = []
    replica_contents = []
    source_dirs = []
    replica_dirs = []

    # Iterate over the content, compare, delete or create
    for root, dirs, files in os.walk(path_to_source):
        for file in files:
            full_file_path = f"{root}{SEP}{file}"
            relative_file_path = full_file_path.replace(f"{path_to_source}{SEP}", "")
            source_contents.append(relative_file_path)
        for dir in dirs:
            full_file_path = f"{root}{SEP}{dir}"
            relative_file_path = full_file_path.replace(f"{path_to_source}{SEP}", "")
            source_dirs.append(relative_file_path)

    for root, dirs, files in os.walk(path_to_replica):
        for file in files:
            full_file_path = f"{root}{SEP}{file}"
            relative_file_path = full_file_path.replace(f"{path_to_replica}{SEP}", "")
            replica_contents.append(relative_file_path)

            if relative_file_path not in source_contents:
                os.remove(full_file_path)
                print(f"File {full_file_path} was deleted in the replica folder")
                changed_files.append(
                    [date.today(), author, "deletion", relative_file_path, "File"]
                )
        for dir in dirs:
            full_dir_path = f"{root}{SEP}{dir}"
            relative_dir_path = full_dir_path.replace(f"{path_to_replica}{SEP}", "")
            replica_contents.append(relative_dir_path)
            if relative_dir_path not in source_dirs:
                shutil.rmtree(full_dir_path)
                print(f"Folder {full_dir_path} was deleted in the replica folder")
                changed_files.append(
                    [date.today(), author, "deletion", full_dir_path, "Folder"]
                )
            else:
                replica_dirs.append(relative_dir_path)

    for root, dirs, files in os.walk(path_to_source):
        for file in files:
            full_file_path = f"{root}{SEP}{file}"
            relative_file_path = full_file_path.replace(f"{path_to_source}{SEP}", "")
            if relative_file_path not in replica_contents:
                file_to_copy = f"{path_to_source}{SEP}{relative_file_path}"
                copy_destination = f"{path_to_replica}{SEP}{relative_file_path}"
                os.makedirs(os.path.dirname(copy_destination), exist_ok=True)
                shutil.copyfile(
                    file_to_copy,
                    copy_destination,
                )
                print(f"File {file} was copied to the replica folder")
                changed_files.append(
                    [date.today(), author, "creation", relative_file_path, "File"]
                )
            else:
                # Check the file content. Copy if different
                if not check_content(
                    f"{path_to_replica}{SEP}{relative_file_path}"
                ) == check_content(f"{path_to_source}{SEP}{relative_file_path}"):
                    file_to_copy = f"{path_to_source}{SEP}{relative_file_path}"
                    copy_destination = f"{path_to_replica}{SEP}{relative_file_path}"
                    shutil.copyfile(
                        file_to_copy,
                        copy_destination,
                    )
                    print(
                        f"File {file} was copied to the replica folder, because the content was different"
                    )
                    changed_files.append(
                        [
                            date.today(),
                            author,
                            "copied because the content was different",
                            relative_file_path,
                            "File",
                        ]
                    )

        for dir in dirs:
            full_dir_path = f"{root}{SEP}{dir}"
            relative_dir_path = full_dir_path.replace(f"{path_to_source}{SEP}", "")
            if relative_dir_path not in replica_dirs:
                source_dir_path = f"{root}{SEP}{dir}"
                dir_to_make = source_dir_path.replace(path_to_source, path_to_replica)
                os.makedirs(dir_to_make, exist_ok=True)
                print(f"Folder {dir} was copied to the replica folder")
                changed_files.append(
                    [date.today(), author, "creation", relative_dir_path, "Folder"]
                )

    # Headers for the csv report
    headers = ["Date", "Author", "Action", "File name", "Type"]

    # Check if there is a report with the same name and generate an index if so
    files_in_directory = os.listdir(".")
    index = ""
    if files_in_directory.count("report.csv") > 0:
        index = files_in_directory.count("report.csv")
    if f"report{index}.csv" in files_in_directory:
        while f"report{index}.csv" in files_in_directory:
            index = index + 1

    # Write the report
    with open(f"report{index}.csv", "w", newline="") as report:
        writer = csv.writer(report)
        writer.writerow(headers)
        for row in changed_files:
            writer.writerow(row)


# It gives you to input the data only if the function is ran within this file
if __name__ == "__main__":
    path_to_source = input("Path to the source folder: ")
    path_to_replica = input("Path to the replica folder: ")
    author = input("Your name: ")

    delete_or_create_and_create_report(path_to_source, path_to_replica, author)
