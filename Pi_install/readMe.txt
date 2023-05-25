To install the project please copy the bash scripts "install.sh" and "run.sh" onto a disk on key and insert it into the raspberry pi (running raspbianOS).
Then copy the file from the disk on key to a directory of your choice on the Pi where you want the project directory to be installed.

It would be best to create a new directory for this program to run and save all it's files in.
for example:

"mkdir -p ~/facial_rec/ ; cd ~/facial_rec/"

Once you did that please run the following commands:

Step 1:

"cd <location_of_the_install.sh_file>"     # example is "cd ~/project/install.sh" where project is a directory that I created in my home directory and copied the file to it.

Step 2:
"bash <location_of_the_install.sh_file>"   # example is "bash ~/project/install.sh"

That's it! the project installation will take a long time since there are heavy libraries needed to install. Please make sure that the raspberry is connected to the internet for the install.

Step 3:
To run the program simply run the following command in the install directory of the program:

"bash run.sh" the program should run without any issues.