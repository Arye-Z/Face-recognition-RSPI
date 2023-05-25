import PySimpleGUI as sg
import os


def valid_id(id: int = 0):
    """
    Function that checks if the ID inputted is valid.
    Args:
        id: Inputted ID of user.

    Returns: Boolean True if user ID is valid.

    """
    if id == "":
        sg.Popup(f"You must enter information in ID field.")
        return False
    if not str(id).isdecimal():
        sg.Popup(f"ID must have only numbers!")
        return False
    if len(id) != 9:
        sg.Popup(f"ID must have exactly 9 digits.")
        return False
    return True


def valid_username(username: str = ""):
    """
    Function that checks if the user name inputted is valid, ie. it is at least one charactor long
    Args:
        username: String of user name

    Returns: Boolean True if user name valid

    """
    if username == "":
        sg.Popup(f"You must enter at least one character as a user name.")
        return False
    return True


def valid_input(values):
    """
    Function to check that the input values for the user are ok.

    Args:
        values: List of values inputted by user.

    Returns: Boolean value.

    """
    return valid_username(values[0]) and valid_id(values[1])  # will only return true if both functions return true


def input_data():
    """
    Function to get from user input data of ID and Username in a popup window gui.

    Returns: User inputted values.

    """
    layout = [
        [sg.Text('Please enter your Name and ID number')],
        [sg.Text('Name', size=(15, 1)), sg.InputText()],
        [sg.Text('ID', size=(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel(), sg.VSeparator(), sg.Help()]
    ]
    window = sg.Window('Simple data entry window', layout, location=(750, 400))
    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED, "Cancel"]:
            values = None
            break
        if event == "Help":
            sg.Popup("User name cannot be blank.\nID must be only 9 digits long and values between 0-9.")
        if event == "Submit":
            if not valid_input(values):
                continue
            else:
                print("[ INFO ] Valid user data input")
                break
    window.close()
    return values


def find_path_to(name_of_folder):
    """ Function to find the folder needed above current folder and path to that folder. """
    i = 1
    temp_path = '.'
    while True:
        if os.path.basename(temp_path) == name_of_folder:
            return temp_path
        temp_path = os.path.realpath(os.path.join(os.getcwd(), os.path.sep.join(['..'] * i)))
        i += 1  # look one folder up
