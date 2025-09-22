#!/bin/bash

read -p "Do you want to generate a new data file (yes/no) : " response

# Vérifie la réponse
if [ "$response" = "yes" ]; then
    python3 datacreation.py
fi

python3 garytree.py