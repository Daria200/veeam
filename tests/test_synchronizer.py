import os
import shutil


from synchronizer import delete_or_create_and_create_report


def test_delete_or_create_and_create_report():

    # The paths and names
    path_to_source = "./tests/folders_to_test/source"
    path_to_replica = "./tests/folders_to_test/replica"
    author = "Me"

    # Delete the folders with test folders if it exists
    if "folders_to_test" in os.listdir("./tests"):
        shutil.rmtree("./tests/folders_to_test")

    # Create a folder for the future source and replica folders
    directory = "folders_to_test"
    parent_dir = "./tests"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    # Create the source folder
    directory = "source"
    parent_dir = "./tests/folders_to_test"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    # Write files in the copy directory
    with open(f"{path_to_source}/file1_to_copy.txt", "w") as file:
        file.write("Text")

    with open(f"{path_to_source}/file.txt", "w") as file:
        file.write("Text")

    os.mkdir(f"{parent_dir}/source/folder_to_copy")

    # Create the replica folder
    directory = "replica"
    parent_dir = "./tests/folders_to_test"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    # Create files in the replica folder
    with open(f"{path_to_replica}/file1_to_delete.txt", "w") as file:
        file.write("Text")

    with open(f"{path_to_replica}/file.txt", "w") as file:
        file.write("Text")

    delete_or_create_and_create_report(path_to_source, path_to_replica, author)

    files_in_source = os.listdir(path_to_source)
    print(files_in_source)
    files_in_replica = os.listdir(path_to_replica)
    print(files_in_replica)
    assert len(files_in_source) == len(files_in_replica)
    assert "file1_to_copy.txt" in files_in_replica
    assert "file1_to_delete.txt" not in files_in_replica
    assert "file.txt" in files_in_replica
    assert "file.txt" in files_in_source
    assert "file1_to_copy.txt" in files_in_source
