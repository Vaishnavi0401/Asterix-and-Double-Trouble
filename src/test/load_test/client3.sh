#!/bin/bash

# Run the instances of the Python client script in the background
cd ../Client
python3 client.py --prob 0.8 &
python3 client.py --prob 0.8 &
python3 client.py --prob 0.8

# Optionally, you can wait for all processes to finish
wait