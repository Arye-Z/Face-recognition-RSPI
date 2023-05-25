import shutil
import time
import cv2
import os
import PySimpleGUI as sg
import face_recognition
from BasicDetectionWithGUI.enterData.getData import input_data
from usefulTools.tools import remove_user_from_db, user_exist

# create the simple gui that will house our image capture
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
# Create the window
window = sg.Window("OpenCV Image Capture", layout, location=(150, 75))

# database classifier

# initialize the video stream, allow the camera sensor to warm up,
# and initialize the total number of example faces written to disk
# thus far
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(0)
time.sleep(2.0)
user_id = ""
pics_dir = ""
user_id_exists = False
total = 0
directions = ["center", "left", "right", "upwards", "downwards"]
total = 0
users_dir = os.path.join(os.getcwd(), os.path.sep.join(['..'] * 2), 'Data', 'Users')
database = os.path.join(os.getcwd(), os.path.sep.join(['..'] * 2), 'Data', 'db.csv')

# loop over the frames from the video stream
while True:
    # info for the gui to run the window
    event, values = window.read(timeout=20)
    # Terminate gui
    if event == "Exit" or event == sg.WIN_CLOSED:
        # print the total faces saved and do a bit of cleanup
        print("[INFO] {} face images stored".format(total))
        print("[INFO] cleaning up...")
        vs.release()  # stop the video capturing
        cv2.destroyAllWindows()  # terminate all openCV windows
        window.close()  # Close GUI window
        break
    # grab the frame from the threaded video stream, clone it, (just
    # in case we want to write it to disk), and then resize the frame
    # so we can apply face detection faster
    _, frame = vs.read()
    orig = frame

    # detect faces in the grayscale frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rects = face_recognition.face_locations(rgb, model='hog')
    # loop over the face detections and draw them on the frame
    if rects:
        cv2.rectangle(frame, (rects[0][1], rects[0][0]), (rects[0][3], rects[0][2]), (0, 255, 0), 2)
    # convert frame to bytecode for display in gui window
    image_bytes = cv2.imencode(".png", cv2.flip(frame, 1))[1].tobytes()
    # Update the image in the GUI window with the image captured
    window["-IMAGE-"].update(data=image_bytes)

    if event == "New User":
        new_user_created = False  # to know if this is a new user to record
        try:
            user_id = input_data()[1]
        except TypeError:
            print("[ WARN ] Something went wrong with new user")
            continue  # this means that the user clicked cancel on enter data popup window
        if not (os.path.exists(users_dir)):
            os.mkdir(users_dir, 777)  # if it does not exist create it with fully open permissions
            print("Users database does not exist, creating output directory...")
        pics_dir = os.path.join(users_dir, user_id)  # new path to user dir
        if not (os.path.exists(pics_dir)):
            os.mkdir(pics_dir, 777)  # if it does not exist create it with fully open permissions
            print("User does not exist, creating user directory...")
            new_user_created = True
            user_id_exists = True
            total = 0
            sg.Popup(
                f"Turn your head {directions[total]} and make sure that you seen the green square and press Capture.")
        if user_id in os.listdir(users_dir) and not new_user_created:
            # if this is not the first time creating the user tell user to start capturing images
            sg.Popup("User exists already, please log in as an existing user or create a new user.")
            # the following forces user to log in by using existing user. !!(might need a better way to do this)
            user_id_exists = False

    if event == "Existing User":
        try:
            user_id = input_data()[1]
        except TypeError:
            continue  # this means that the user clicked cancel on enter data popup window
        if user_exist(user_id, users_dir):
            overwrite = True if sg.popup_yes_no(
                "User exists.\nDo you want to overwrite the data for this user?") == "Yes" else False
            if overwrite:
                # first we need to remove the previous users encodings from the database
                remove_user_from_db(user_id, database)
                total = 0
                user_id_exists = True
                pics_dir = os.path.join(users_dir, user_id)  # where to save the new pictures that will be captured
                sg.Popup(
                    f"Turn your head {directions[total]} and make sure that you seen the green square.")
                # force the user to start the capturing process
        else:
            sg.Popup("User does not exist, please create a new user.")

    if event == "Capture":
        if not user_id_exists:
            sg.Popup("Please choose an existing user or create a new user.")
            continue
        if total == 5:
            sg.Popup("You have already taken all the pics needed, to re-do please press Re-Capture.")
            continue
        if len(rects): # only if the persons face is
            if (abs(rects[0][0]-rects[0][2]) < 300): #Only if the person is close enough
                sg.Popup("Get close to the camera")
                continue
                print(rects)
            print(f"Saving image for {directions[total]}...")
            output = os.path.join(pics_dir, "{}.png".format(str(directions[total])))
            _, frame = vs.read()
            orig = frame
            cv2.imwrite(output, orig)
            total += 1
            if total < 5:
                sg.Popup(f"Turn your head {directions[total]} and make sure that you seen the green square.")
            else:
                sg.Popup("Done!")
        elif not len(rects):
            sg.Popup("Face was not recorded, please try again.")

    if event == "Re-Capture":
        if total:  # at least one pic has been created
            total = 0  # restart the count of pics
            user_pics_dir = os.path.join(users_dir, user_id)  # location of the user's pics
            for filename in os.listdir(user_pics_dir):
                if filename.endswith(".png"):  # only delete the images saved
                    file_path = os.path.join(user_pics_dir, filename)
                    # try deleting the files
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            sg.Popup("No images were captured or user has not been created or chosen.\n You can not use this function.")

    if event == "Erase User":
        try:
            user_id = input_data()[1]
        except TypeError:
            continue  # this means that the user clicked cancel on enter data popup window
        delete_path = os.path.join(users_dir, user_id)
        if user_id and os.path.exists(delete_path) and os.path.isdir(delete_path):
            if sg.popup_yes_no("Are you sure you want to proceed? once deleted cannot be undone...") == "Yes":
                try:
                    remove_user_from_db(user_id, database)  # remove user from encoding database
                    shutil.rmtree(delete_path)  # delete all user files
                except Exception as e:
                    sg.Popup("Could not delete, please contact developers.")
                    print(f"Failed to delete {delete_path}. Reason: {e}")
                    exit(1)
                sg.Popup("User was removed successfully.")
        else:
            sg.Popup("Could not delete user, user does not exist in database.")

    if event == "Help":
        pass  # TODO need to implement a help button for the user to know what each option does
