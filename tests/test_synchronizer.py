import sys
import os
import shutil


from synchronizer import delete_or_create_and_create_report


def test_delete_or_create_and_create_report():
    path_to_source = "./source"
    path_to_replica = "./replica"
    author = "Me"

    if "folders_to_test" in os.listdir("./tests"):
        shutil.rmtree("./tests/folders_to_test")

    directory = "folders_to_test"
    parent_dir = "./tests"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
