#!/bin/bash

# Run the instances of the Python client script in the background
cd ../Client
python3 client.py --prob 0.4 &
python3 client.py --prob 0.4 &
python3 client.py --prob 0.4 &
python3 client.py --prob 0.4 &
python3 client.py --prob 0.4

# Optionally, you can wait for all processes to finish
wait