#!/bin/bash

read -p "Do you want to generate a new data file (yes/no) : " response

if [ "$response" = "yes" ]; then
    python3 code/datacreation.py
fi

python3 code/garytree.py