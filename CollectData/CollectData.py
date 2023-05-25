from BasicDetectionWithGUI.MainGUI.MainGUI import ImageCaptureGUI
from EncodingFaces.encoding import EncodingDB


class CollectData:
    def __init__(self):
        self.gui = ImageCaptureGUI()
        self.encoding = EncodingDB()

    def collectData(self):
        """
        Main function collecting user data.
        Steps for collection and processing each user added, changed or removed from the data base are:
        First the image capturing gui is run with options for adding, changing or removing users.
        Then the encoding is run over the images collected from all new or existing user images and if the user is new, adds it to the database,
        if the user already exists in the data base it will not add the pictures a second time.
        Returns:

        """
        # run the main gui for collecting and manipulation users in data base.
        self.gui.mainLoop()
        # run encoding of the pictures that have been added to the data base.
        self.encoding.mainEncode()

# if __name__ == '__main__':
#     collect_data = CollectData()
#     collect_data.collectData() # run the data collection
