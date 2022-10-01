import os
import shutil


from synchronizer import delete_or_create_and_create_report


def test_delete_or_create_and_create_report():
    path_to_source = "./tests/folders_to_test/source"
    path_to_replica = "./tests/folders_to_test/replica"
    author = "Me"

    if "folders_to_test" in os.listdir("./tests"):
        shutil.rmtree("./tests/folders_to_test")

    directory = "folders_to_test"
    parent_dir = "./tests"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    print(os.listdir("./tests"))

    directory = "source"
    parent_dir = "./tests/folders_to_test"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    with open(f"{path_to_source}/file1_to_copy.txt", "w") as file:
        file.write("Text")

    with open(f"{path_to_source}/file.txt", "w") as file:
        file.write("Text")

    directory = "replica"
    parent_dir = "./tests/folders_to_test"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    with open(f"{path_to_replica}/file1_to_delete.txt", "w") as file:
        file.write("Text")

    with open(f"{path_to_replica}/file.txt", "w") as file:
        file.write("Text")

    delete_or_create_and_create_report(path_to_source, path_to_replica, author)

    files_in_source = os.listdir(path_to_source)
    files_in_replica = os.listdir(path_to_replica)
    assert len(files_in_source) == len(files_in_replica)
    assert "file1_to_copy.txt" in files_in_replica
    assert "file1_to_delete.txt" not in files_in_replica
    assert "file.txt" in files_in_replica
    assert "file.txt" in files_in_source
    assert "file1_to_copy.txt" in files_in_source
