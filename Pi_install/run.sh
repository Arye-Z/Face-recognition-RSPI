#!/bin/bash

cd ./Embedded_CV/
mkdir -p ./Data/UserNames
cd ./Main/
python3.8 ./main.py
cd ../../
echo "done running program"