import shutil
import sys
import time
import cv2
import os
import PySimpleGUI as sg
import face_recognition
from BasicDetectionWithGUI.enterData.getData import input_data, find_path_to
from usefulTools.tools import remove_user_from_db, user_exist, delete_pics, remove_user_name
from BasicDetectionWithGUI.createGUI.buildGUI import createGUI


class ImageCaptureGUI:
    def __init__(self):
        # Create the GUI window
        self.window = createGUI()
        # initialize the video stream, allow the camera sensor to warm up,
        # and initialize the self.total number of example faces written to disk
        # thus far
        print("[INFO] starting video stream...")
        self.vs = cv2.VideoCapture(0)
        time.sleep(2.0)
        self.user_id = ""
        self.pics_dir = ""
        self.user_id_exists = False
        self.directions = ["center", "left", "right", "upwards", "downwards"]
        self.total = 0
        self.project_path = find_path_to("Embedded_CV")
        self.users_dir = os.path.join(self.project_path, 'Data', 'Users')
        self.user_names_loc = os.path.join(self.project_path, 'Data', 'UserNames')
        self.database = os.path.join(self.project_path, 'Data', 'db.csv')
        self.userName = ""

    # loop over the frames from the video stream
    def mainLoop(self):
        """
        Main loop for running data collection GUI to add, change or remove users from the user data base.
        Returns: None

        """
        while True:
            # info for the gui to run the window
            event, values = self.window.read(timeout=20)
            # Terminate gui
            if event == "Exit" or event == sg.WIN_CLOSED:
                # print the self.total faces saved and do a bit of cleanup
                print("[INFO] {} face images stored".format(self.total))
                print("[INFO] cleaning up...")
                try:
                    self.vs.release()  # stop the video capturing
                    cv2.destroyAllWindows()  # terminate all openCV windows
                    self.window.close()  # Close GUI window
                except cv2.error as e:
                    pass
                finally:
                    break
            # grab the frame from the threaded video stream, clone it, (just
            # in case we want to write it to disk), and then resize the frame
            # so we can apply face detection faster
            _, frame = self.vs.read()
            # detect faces in the grayscale frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rects = face_recognition.face_locations(rgb, model='hog')
            # loop over the face detections and draw them on the frame
            if rects:
                cv2.rectangle(frame, (rects[0][1], rects[0][0]), (rects[0][3], rects[0][2]), (0, 255, 0), 2)
            # convert frame to bytecode for display in gui window
            image_bytes = cv2.imencode(".png", cv2.flip(frame, 1))[1].tobytes()
            # Update the image in the GUI window with the image captured
            self.window["-IMAGE-"].update(data=image_bytes)

            if event == "New User":
                new_user_created = False  # to know if this is a new user to record
                try:
                    inputuserdata = input_data()
                    self.userName = inputuserdata[0]
                    self.user_id = inputuserdata[1]
                except TypeError:
                    print("[ WARN ] Something went wrong with new user")
                    continue  # this means that the user clicked cancel on enter data popup window
                if not (os.path.exists(self.users_dir)):
                    os.mkdir(self.users_dir, 0o777)  # if it does not exist create it with fully open permissions
                    print("Users self.database does not exist, creating output directory...")
                self.pics_dir = os.path.join(self.users_dir, self.user_id)  # new path to user dir
                if not (os.path.exists(self.pics_dir)):
                    os.mkdir(self.pics_dir, 0o777)  # if it does not exist create it with fully open permissions
                    print("User does not exist, creating user directory...")
                    # check if user names directory exists and create it if not
                    if not (os.path.exists(self.user_names_loc)):
                        os.mkdir(self.user_names_loc, 0o777)
                    # add username to user name data folder
                    with open(os.path.join(self.user_names_loc, f"{self.user_id}.txt"), 'w') as f:
                        f.write(self.userName)
                    new_user_created = True
                    self.user_id_exists = True
                    self.total = 0
                    sg.Popup(
                        f"Turn your head {self.directions[self.total]} and make sure that you seen the green square and press Capture.")
                if self.user_id in os.listdir(self.users_dir) and not new_user_created:
                    sg.Popup("User exists already, please log in as an existing user or create a new user.")
                    self.user_id_exists = False

            if event == "Existing User":
                try:
                    inputuserdata = input_data()
                    self.userName = inputuserdata[0]
                    self.user_id = inputuserdata[1]
                except TypeError:
                    continue  # this means that the user clicked cancel on enter data popup window
                if user_exist(self.user_id, self.database):
                    overwrite = True if sg.popup_yes_no(
                        "User exists.\nDo you want to overwrite the data for this user?") == "Yes" else False
                    if overwrite:
                        # first we need to remove the previous users encodings from the database
                        remove_user_from_db(self.user_id, self.database)
                        delete_pics(self.user_id, self.users_dir)
                        self.total = 0
                        self.user_id_exists = True
                        self.pics_dir = os.path.join(self.users_dir,
                                                     self.user_id)  # where to save the new pictures that will be captured
                        sg.Popup(
                            f"Turn your head {self.directions[self.total]} and make sure that you seen the green square.")
                        # force the user to start the capturing process
                else:
                    sg.Popup("User does not exist, please create a new user.")

            if event == "Capture":
                if not self.user_id_exists:
                    sg.Popup("Please choose an existing user or create a new user.")
                    continue
                if self.total == 5:
                    sg.Popup("You have already taken all the pics needed, to re-do please press Re-Capture.")
                    continue
                if len(rects):  # only if the persons face is
                    if abs(rects[0][0] - rects[0][2]) < 175:  # Only if the person is close enough
                        sg.Popup("Get close to the camera")
                        continue
                        print(rects)
                    # print(f"Saving image for {self.directions[self.total]}...")
                    output = os.path.join(self.pics_dir, "{}.png".format(str(self.directions[self.total])))
                    # _, frame = self.vs.read()
                    # orig = frame
                    cv2.imwrite(output, frame)
                    self.total += 1
                    if self.total < 5:
                        sg.Popup(
                            f"Turn your head {self.directions[self.total]} and make sure that you seen the green square.")
                    else:
                        sg.Popup("Done!")
                        print("[ INFO ] Validating images were saved to disk...\n")
                        time_counter = 1
                        while not os.path.exists(self.pics_dir) and len(os.listdir(self.pics_dir)) == 0:
                            time.sleep(0.5)
                            print(f"Checking images...Please wait{time_counter * '.'}", end='\r')
                        print("[ INFO ] Images were saved successfully")
                elif not len(rects):
                    sg.Popup("Face was not recorded, please try again.")

            if event == "Re-Capture":
                if self.total:  # at least one pic has been created
                    self.total = 0  # restart the count of pics
                    user_self.pics_dir = os.path.join(self.users_dir, self.user_id)  # location of the user's pics
                    for filename in os.listdir(user_self.pics_dir):
                        if filename.endswith(".png"):  # only delete the images saved
                            file_path = os.path.join(user_self.pics_dir, filename)
                            # try deleting the files
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                print('Failed to delete %s. Reason: %s' % (file_path, e))
                else:
                    sg.Popup(
                        "No images were captured or user has not been created or chosen.\n You can not use this function.")

            if event == "Erase User":
                try:
                    inputuserdata = input_data()
                    self.userName = inputuserdata[0]
                    self.user_id = inputuserdata[1]
                except TypeError:
                    continue  # this means that the user clicked cancel on enter data popup self.window
                delete_path = os.path.join(self.users_dir, self.user_id)
                if self.user_id and os.path.exists(delete_path) and os.path.isdir(delete_path):
                    if sg.popup_yes_no("Are you sure you want to proceed? once deleted cannot be undone...") == "Yes":
                        try:
                            remove_user_name(self.user_id, self.user_names_loc)
                            remove_user_from_db(self.user_id, self.database)  # remove user from encoding self.database
                            shutil.rmtree(delete_path)  # delete all user files
                        except Exception as e:
                            sg.Popup("Could not delete, please contact developers.")
                            # print(f"Failed to delete {delete_path}. Reason: {e}")
                            sys.stderr.write(f"Failed to delete {delete_path}. Reason: {e}")
                            continue
                        sg.Popup("User was removed successfully.")
                else:
                    sg.Popup("Could not delete user, user does not exist in self.database.")

            if event == "Help":
                pass  # TODO need to implement a help button for the user to know what each option does
