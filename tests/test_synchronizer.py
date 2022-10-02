import os
import shutil


from synchronizer import delete_or_create_and_create_report, check_content


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

    # Write files in the source directory
    # Create folders that exists in the replica folder as well
    os.mkdir(f"{parent_dir}/source/folder_with_content")
    os.mkdir(f"{parent_dir}/source/folder_with_content/folder")
    os.mkdir(f"{parent_dir}/source/empty_folder")

    # Create file that exists in the replica folder as well
    with open(f"{path_to_source}/style.css", "w") as file:
        file.write("Text")

    # Create folders to copy
    os.mkdir(f"{parent_dir}/source/folder_with_content_to_copy")
    os.mkdir(f"{parent_dir}/source/folder_with_content_to_copy/folder")
    os.mkdir(f"{parent_dir}/source/empty_folder_to_copy")

    # Create file to copy
    with open(f"{path_to_source}/file_to_copy.py", "w") as file:
        file.write("Text")
    with open(f"{path_to_source}/overwrite.txt", "w") as file:
        file.write("This is the right text")

    # Create the replica folder
    directory = "replica"
    parent_dir = "./tests/folders_to_test"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    # Create folders in the replica folder that exist in the source folder as well
    os.mkdir(f"{parent_dir}/replica/folder_with_content")
    os.mkdir(f"{parent_dir}/replica/folder_with_content/folder")
    os.mkdir(f"{parent_dir}/replica/empty_folder")

    # Create file in the replica folder that exist in the source folder as well
    with open(f"{path_to_replica}/style.css", "w") as file:
        file.write("Text")
    with open(f"{path_to_replica}/overwrite.txt", "w") as file:
        file.write("This the wrong text")

    # Create files and folders to delete
    with open(f"{path_to_replica}/file_to_delete.py", "w") as file:
        file.write("Text")
    os.mkdir(f"{parent_dir}/replica/folder_to_delete")
    os.mkdir(f"{parent_dir}/replica/folder_to_delete/folder1")
    os.mkdir(f"{parent_dir}/replica/empty_folder_to_delete")

    delete_or_create_and_create_report(path_to_source, path_to_replica, author)

    files_in_source = os.listdir(path_to_source)
    files_in_replica = os.listdir(path_to_replica)

    # assert both directories have the same amount of files
    assert len(files_in_source) == len(files_in_replica)

    # Check the content of the repilca folder
    assert "folder_with_content" in files_in_replica
    assert "empty_folder" in files_in_replica
    assert "style.css" in files_in_replica
    assert "empty_folder_to_copy" in files_in_replica
    assert "file_to_copy.py" in files_in_replica
    assert "folder_with_content_to_copy" in files_in_replica

    # Check redundant files were deleted
    assert "file_to_delete.py" not in files_in_replica
    assert "empty_folder_to_delete" not in files_in_replica
    assert "folder_to_delete" not in files_in_replica

    assert check_content(f"{path_to_source}/overwrite.txt") == check_content(
        f"{path_to_replica}/overwrite.txt"
    )

    # Check the content of the source folder
    assert "folder_with_content" in files_in_source
    assert "empty_folder" in files_in_source
    assert "style.css" in files_in_source
    assert "empty_folder_to_copy" in files_in_source
    assert "file_to_copy.py" in files_in_source
    assert "folder_with_content_to_copy" in files_in_source
    assert "file_to_delete.py" not in files_in_source
    assert "empty_folder_to_delete" not in files_in_source
    assert "folder_to_delete" not in files_in_source
