@ECHO OFF
echo installing requirements for project

rem we need to make sure that cmake and boost are installed for face-recognition module
rem pip install boost
rem pip install cmake
rem install the rest of the requirements by this project
pip install -r requirements.txt

echo done installing