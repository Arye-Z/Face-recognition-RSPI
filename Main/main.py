import os
import sys

# adding project directory to system paths for running local project packages for use when not running through Pycharm env
project_path = os.path.abspath(os.path.join(__file__, "..", ".."))
if project_path not in sys.path and os.path.basename(project_path) == "Embedded_CV":
    sys.path.append(project_path)

from CollectData.CollectData import CollectData  # nopep8
from RealTime import RealTime as rt, testing_training as tt  # nopep8

if __name__ == '__main__':
    options = "Please choose a running mode:" \
              "\n1. Data Collection" \
              "\n2. Real Time" \
              "\n3. Training Mode" \
              "\n4. Exit Program" \
              "\n"
    while True:
        mode = int(input(options))
        if mode == 1:
            collect_data = CollectData()
            # run collect data and encode data to add, change or remove people from the data base
            collect_data.collectData()
        elif mode == 2:
            running_mode = rt.RealTime()
            # run the real time mode of constant face comparisons vs the data base on faces in front of camera
            running_mode.mainRun()
        elif mode == 3:
            with_prints = True if input("Do you want to print graphs of the training? [y/n]") == 'y' else False
            training = tt.Training()
            training.train()
            training.calculate_avg()
            if with_prints:
                training.print_graphs()
        elif mode == 4:
            print("[ INFO ] Exiting program.")
            exit(0)
        else:
            print("You chose a value not in the list [1,2,3,4] please choose a valid option.")
