import PySimpleGUI as sg


def createGUI(gui_title="OpenCV Image Capture", window_location=(0, 0)):
    """
    Function for creating main data collection gui.

    Args:
        gui_title: Title for the GUI window.
        window_location: X and Y coordinates for the GUI window to be placed on screen.

    Returns: Return GUI window created and build for use in program.

    """
    # set gui background color
    sg.theme("DarkBlue")
    # Define the window layout
    vid_col = [
        [sg.Text("Camera - Main", size=(100, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
    ]
    option_col = [
        [sg.Button("New User", size=(10, 1))],
        [sg.Button("Existing User", size=(10, 1))],
        [sg.Button("Capture", size=(10, 1))],
        [sg.Button("Re-Capture", size=(10, 1))],
        [sg.Button("Erase User", size=(10, 1))],
        [sg.Button("Exit", size=(10, 1))],
    ]
    layout = [
        [
            sg.Frame("Live video feed", vid_col),
            sg.VSeparator(),
            sg.Frame("Options", option_col)
        ]
    ]
    window = sg.Window(gui_title, layout, location=window_location)
    return window
