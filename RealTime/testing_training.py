"""
Explanation: The purpose of the code is to study the differences between people
The way to do this is by calculating Euclidean distance between two vectors representing a person's face
If the face is identical the ideal is that the Euclidean distance between them will be 0
But if they are different the ideal is that the normalized distance between them will be 1
If the distance between 2 vectors representing the same person is greater than 0 then the line
separating them will have less safety distance. Etc. for vectors of different people when the distance is not 1
For this purpose we took the database and divided it into 10 parts
Each time we check the distance between a tenth of the chosen ones and the rest
The loop will run 10 times so that each time they will take a different tenth
We will keep all distances of all 10 runs and their average will be the distance that marks the line
between vectors of the same or different people
"""

import os
from usefulTools.tools import read_encoding
import random
import numpy as np
from matplotlib import pyplot as plt
from time import process_time
from BasicDetectionWithGUI.enterData.getData import find_path_to

# *********** GLOBAL PATHS **********
project_path = find_path_to("Embedded_CV")  # project dir path that we can access all sub folders from
db_path = os.path.join(project_path, 'Data', 'db.csv')
tolerance_file = os.path.join(project_path, "Data", "tolerance.txt")


class Training:
    def __init__(self):
        self.iterations = 150  # Varies to determine the maximum iterations
        self.cross = 10  # Varies to determine how many parts the information will be divided into
        self.y_Euclidean = []
        self.y_Manhattan = []
        self.times = []  # To view the calculation times of the loops
        self.average_manhattan = 0
        self.average_euclidean = 0
        self.enc_file = np.array(read_encoding(db_path))

    @staticmethod
    def Manhattan_distance(vector_A, vector_B):
        """
        Function for calculating distance from Manhattan
        Args:
            vector_A: First vector of data
            vector_B: Second vector of data

        Returns: Sum of the absolute distance between the 2 vectors

        """
        tot = 0
        for i in range(128):
            tot += abs(vector_A[i] - vector_B[i])
        return tot

    @staticmethod
    def save_tolerance(tolerance):
        with open(tolerance_file, 'w') as f:
            f.write(str(tolerance))

    def calculate_avg(self):
        average_manhattan = sum(self.y_Manhattan) / len(self.y_Manhattan)
        average_euclidean = sum(self.y_Euclidean) / len(self.y_Euclidean)
        Training.save_tolerance(average_euclidean)  # save the Euclidean average to our tolerance file
        print(f"The average of all runs for Euclidean distance: {average_manhattan}")
        print(f"The average of all runs for Manhattan distance: {average_euclidean}")

    def print_graphs(self):
        fig, axs = plt.subplots(2)
        fig.suptitle('"Graph of number of learning cycles vs accuracy of results."', color='b')
        axs[0].set_ylabel('Euclidean', color='g')
        axs[0].set_title("Accuracy in Euclidean distance", color='g')
        axs[0].plot(self.x, self.y_Euclidean)
        axs[1].set_ylabel('Manhattan', color='g')
        axs[1].set_title("Accuracy in Manhattan distance", color='g')
        axs[1].plot(self.x, self.y_Manhattan)
        plt.show()
        plt.plot(self.x, self.times)
        plt.ylabel("time")
        plt.xlabel("iteration")
        plt.show()

    def train(self):
        for rng in range(1, self.iterations):
            print(rng)
            t1_start = process_time()
            sum_Euclidean = 0
            sum_Manhattan = 0

            for i in range(rng):
                match_res_Euclidean = 0  # for 2 options -  equal and different ID numbers
                no_match_res_Euclidean = 1

                match_res_Manhattan = 0  # for 2 options -  equal and different ID numbers
                no_match_res_Manhattan = 1

                sum_of_lines_Euclidean = []  # to Keep all distances in all ten runs
                sum_of_lines_Manhattan = []

                mixed = []
                for s in random.sample(range(0, len(self.enc_file)), len(self.enc_file)):  # Create an array of mixed numbers
                    mixed.append(s)

                for choice in range(0, len(mixed) - 1, int(len(self.enc_file) / self.cross)):  # A loop that ran cross times

                    rand = [i for i in mixed[choice:choice + int(len(self.enc_file) / self.cross)]]  # Random selection of one tenth of the data

                    # now delete the random numbers from train and add them to test
                    train = np.delete(self.enc_file, rand, 0)
                    test = np.array([self.enc_file[i] for i in range(len(self.enc_file)) if i in rand])

                    # now We will compare every vectors from test to train

                    for j in range(len(test)):  # Euclidean distance
                        for k in range(len(train)):
                            Euclidean = np.linalg.norm(test[j][1:] - train[k][1:])  # Find the norm distance (Euclidean)
                            # If it's the same person and the distance between 2 vectors is
                            # greater than the distance we know then take the new distance
                            if test[j][0] == train[k][0] and Euclidean > match_res_Euclidean:
                                match_res_Euclidean = Euclidean
                            # Same for identical people
                            if test[j][0] != train[k][0] and Euclidean < no_match_res_Euclidean:
                                no_match_res_Euclidean = Euclidean
                    # For each loop, enter the maximum safety distance into the array
                    sum_of_lines_Euclidean.append(((match_res_Euclidean - no_match_res_Euclidean) / 2) + no_match_res_Euclidean)

                    for j in range(len(test)):  # Manhattan distance
                        for k in range(len(train)):
                            Manhattan = Training.Manhattan_distance(test[j][1:], train[k][1:])
                            if test[j][0] == train[k][0] and Manhattan > match_res_Manhattan:
                                match_res_Manhattan = Manhattan
                            if test[j][0] != train[k][0] and Manhattan < no_match_res_Manhattan:
                                no_match_res_Manhattan = Manhattan
                    sum_of_lines_Manhattan.append(((match_res_Manhattan - no_match_res_Manhattan) / 2) + no_match_res_Manhattan)

                # An average over all safety distances will give the desired distance for this data
                sum_Manhattan += sum(sum_of_lines_Manhattan) / len(sum_of_lines_Manhattan)
                sum_Euclidean += sum(sum_of_lines_Euclidean) / len(sum_of_lines_Euclidean)
            self.y_Manhattan.append(sum_Manhattan / rng)
            self.y_Euclidean.append(sum_Euclidean / rng)
            t1_stop = process_time()
            self.times.append((t1_stop - t1_start))
