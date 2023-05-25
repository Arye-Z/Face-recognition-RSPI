import cv2
import time
import PySimpleGUI as sg
import os
import face_recognition
import threading
import queue
from usefulTools.tools import read_encoding, read_names
from BasicDetectionWithGUI.enterData.getData import find_path_to

# ******* structure of real time GUI ********
vid_col = [
    [sg.Text("Camera - Main", size=(100, 1), justification="center")],
    [sg.Image(filename="", key="-IMAGE-")],
]

layout = [
    [
        sg.Frame("Live video feed", vid_col),
        sg.VSeparator()
    ]
]

# *********** GLOBAL PATHS **********
project_path = find_path_to("Embedded_CV")
tolerance_file = os.path.join(project_path, "Data", "tolerance.txt")


class RealTime:
    def __init__(self):
        self.window = sg.Window("OpenCV Image Capture", layout, location=(150, 75))
        self.tolerance = None
        self._get_tolerance()
        self.encodings = None
        self.names = read_names(os.path.join(project_path, 'Data', 'UserNames'))
        self.encoding_file = read_encoding(os.path.join(project_path, 'Data', 'db.csv'))

    def _get_tolerance(self):
        try:
            with open(tolerance_file, 'r') as f:
                self.tolerance = float(f.readline())
        except FileNotFoundError:
            self.tolerance = 0.6  # default to 0.6 if tolerance file not found and training has not been run

    def compare_to_CSV(self, enc_file, out_queue):
        for i in range(len(enc_file)):
            matches = face_recognition.compare_faces([enc_file[i][1:]], self.encodings, tolerance=self.tolerance)
            if True in matches:
                print(f"\rUser face detected. User ID: {enc_file[i][0]}", end='')
                identify_id = int(enc_file[i][0])  # for text in guy box
                out_queue.put(identify_id)
            else:
                print("\rNo users detected in video.", end='')

    def mainRun(self):
        # open the computer camera
        print("[INFO] starting video stream...")
        vs = cv2.VideoCapture(0)
        time.sleep(2.0)
        time_stop = 1.1
        time_start = 0
        while True:
            # info for the gui to run the window
            event, values = self.window.read(timeout=20)
            if event == "Exit" or event == sg.WIN_CLOSED:
                print("[INFO] cleaning up...")
                vs.release()  # stop the video capturing
                cv2.destroyAllWindows()  # terminate all openCV windows
                self.window.close()  # Close GUI window
                break
            _, frame = vs.read()
            # orig = frame
            # detect faces in the grayscale frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rects = face_recognition.face_locations(rgb, model='hog')
            # loop over the face detections and draw them on the frame
            # We will now encode the face of the camera
            try:
                self.encodings = face_recognition.face_encodings(rgb, rects)[0]
            except IndexError:
                continue  # in the case that there are no faces in frame
            # Compare to CSV file by threading
            if time_stop - time_start > 0.5:
                time_start = time.process_time()
                my_queue = queue.Queue()
                t = threading.Thread(target=self.compare_to_CSV, args=(self.encoding_file, my_queue))
                t.start()
                identify_id = my_queue.get()
            if rects:
                cv2.rectangle(frame, (rects[0][1], rects[0][0]), (rects[0][3], rects[0][2]), (0, 255, 0), 2)
                # to add ID in guy box
                cv2.putText(frame, self.names[identify_id], (rects[0][3], rects[0][0]), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
                # convert frame to bytecode for display in gui window
                image_bytes = cv2.imencode(".png", cv2.flip(cv2.flip(frame, 1), 1))[1].tobytes()
                # Update the image in the GUI window with the image captured
                self.window["-IMAGE-"].update(data=image_bytes)
            else:
                continue
            time_stop = time.process_time()
