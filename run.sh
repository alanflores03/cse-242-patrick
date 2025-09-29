#!/bin/bash

read -p "Do you want to generate new data files (yes/no) : " response

if [ "$response" = "yes" ]; then
    python3 code/datacreation.py
    echo "You can now copy these file names from the generated file (without a number at the end) to the following prompt."
fi

python3 code/blocks.py