import glob
import os
import csv
import shutil
import sys

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def find_images_in_dir(users_pics_dir):
    """
    Find all the images in the user pics dir.

    Args:
        users_pics_dir: Path to users pic directory with saved images of users to encode.

    Returns: List of paths to all the pictures of users currently in the users pics directory.

    """
    imagePaths = []
    for root, dirs, files in os.walk(users_pics_dir, topdown=True):
        if len(files) == 0:
            continue  # empty user
        for file in files:
            if file[file.find('.'):] in image_types:
                imagePaths.append(os.path.join(root, file))
    return imagePaths


def add_encoding_to_csv(userID, values, file_path):
    """
    Function that adds the userId + userName + user facial data to the encoded main data base with all user's data.

    Args:
        userID: ID of user (for 1st column)
        userName: User name of user (for 2nd column)
        values: List object with all encoding values for user image
        file_path: Path to data base csv file

    Returns:

    """
    lines = []
    try:
        with open(file_path, 'r') as readFile:
            reader = list(csv.reader(readFile))
            if len(reader):  # non empty file
                for row in reader:
                    lines.append(row[0])  # only the ID
    except FileNotFoundError:
        pass
    with open(file_path, 'a', newline='') as db:
        write = csv.writer(db)
        # will only add user if the user does not already exist in database which means 5 pics of a specific user
        if lines.count(userID) < 5:
            write.writerow([userID] + values)  # will append to the bottom of the csv file the new user and values


# to read the csv file
def read_encoding(file_path):
    with open(file_path, newline='') as db:
        csvF = csv.reader(db, quoting=csv.QUOTE_NONNUMERIC)
        return [i for i in csvF]


def read_names(name_path):  # A function that pulls all the names and ID into a dictionary
    all_users = os.listdir(name_path)
    user_id = []
    names = []
    for i in all_users:
        user_id.append(int(i[0:9]))
        names.append(open(os.path.join(name_path, i), "r+").read())
    return {user_id[i]: names[i] for i in range(len(user_id))}


def remove_user_from_db(user_id, file_path):
    """
    Function to remove user from the data base.

    Args:
        user_id: ID of user to remove from database
        file_path: Path to datebase

    Returns:

    """
    lines = list()
    with open(file_path, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[0] == user_id:
                lines.remove(row)
    with open(file_path, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)


def delete_pics(user_id, user_pics_loc):
    """
    function to delete user's pics
    Args:
        user_id: user id to remove
        user_pics_loc: path to directory with all user's pics

    Returns: None

    """
    if os.path.exists(os.path.join(user_pics_loc, user_id)):
        files = glob.glob(os.path.join(user_pics_loc, user_id, f"*"))
        for f in files:
            os.remove(f)
    else:
        print("User does not exist.")


def remove_user_name(user_id, user_pics_loc):
    """
    function to remove the user name of a particular id from the data base
    Args:
        user_id: user id to remove
        user_pics_loc: path to directory with all user name files

    Returns: None

    """
    path_to_username = os.path.join(user_pics_loc, f"{user_id}.txt")
    if os.path.exists(path_to_username):
        os.remove(path_to_username)
    else:
        print("User name does not exist.")


def user_exist(user_id, path_to_db):
    """
    Checks if user exists in database.

    Args:
        user_id: User ID to find in database
        path_to_db: Path to the data base file

    Returns: True if user exists otherwise returns False

    """
    with open(path_to_db, 'r') as f:
        user_data = csv.reader(f)
        for user in user_data:
            if user[0] == user_id:
                return True  # User does exists in database
    return False  # User does not exist in database


def images_cleanup(path_to_user_images, user_id):
    delete_path = os.path.join(path_to_user_images, user_id)
    try:
        shutil.rmtree(delete_path)  # delete all user files
    except Exception as e:
        sys.stderr.write("Could not delete, please contact developers.")
        # print(f"Failed to delete {delete_path}. Reason: {e}")
        sys.stderr.write(f"Failed to delete {delete_path}. Reason: {e}")
