import face_recognition
import cv2
import os
# local library with useful tools for functions that repeat in different codes
from usefulTools.tools import find_images_in_dir, add_encoding_to_csv, images_cleanup
from BasicDetectionWithGUI.enterData.getData import find_path_to


class EncodingDB:
    def __init__(self):
        self.bad_encode = {}
        self.knownEncodings = []
        self.knownNames = []
        self.project_path = find_path_to("Embedded_CV")  # project dir path that we can access all sub folders from it
        self.users_dir = os.path.join(self.project_path, 'Data', 'Users')
        self.user_names_loc = os.path.join(self.project_path, 'Data', 'UserNames')
        self.db_path = os.path.join(self.project_path, 'Data', 'db.csv')
        # get paths of each file in folder named Images
        # Images here contains my data(folders of various persons)
        self.imagePaths = None

    def mainEncode(self):
        """
        main function to go over user's pictures and encode them and add the data to the main data base
        :return: 
        """
        success_counter = 0
        users_encoded = []
        print("Starting to encode images... Please wait...")
        self.imagePaths = find_images_in_dir(self.users_dir)
        # loop over the image paths
        for i, imagePath in enumerate(self.imagePaths):
            # extract the person id from the image path
            user_id = imagePath.split(os.path.sep)[-2]
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb, model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            if len(encodings):
                add_encoding_to_csv(userID=user_id, values=list(encodings[0]), file_path=self.db_path)
                success_counter += 1
                if success_counter == 4:
                    success_counter = 0
                    users_encoded.append(user_id)
            else:
                if user_id not in self.bad_encode.keys():
                    self.bad_encode[user_id] = []
                self.bad_encode[user_id].append(imagePath.split(os.path.sep)[-1]) # this user has 1 or more images that aren't encoding properly

        # check if any users had images that did not manage to encode
        for user in self.bad_encode.keys():
            s = 's'
            print(f"User with ID: {user} has {len(self.bad_encode[user])} badly encoded image{'s' if len(self.bad_encode[user]) > 1 else ''}."
                  f" Bad images are: {self.bad_encode[user]}")

        if input("Do you want to delete user images that were encoded successfully? [y/n]\n").lower() == 'y':
            for user in users_encoded:
                images_cleanup(self.imagePaths, user)
        print("Finished encoding images!")
