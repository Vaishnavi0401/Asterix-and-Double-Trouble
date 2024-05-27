

import requests
import argparse
import http.client
import sys
import json
import random
import time
import itertools

# Lookup stock prices
LOOKUP_TEST_SET = [
    # lookup -> 200, valid requests x 5
    "/product/Barbie",
    "/product/Fox",
    "/product/Tux",
    "/product/Monopoly",
    "/product/Elephant",
    # Toy name not found -> error 404, stock not found x 4
    "/product/Book",
    "/product/Pen",
    "/product/Teddy",
    "/product/Train",
    # Invalid URL -> error 400, invalid URL
    "/Teddy/Lego"
]

# Define the main function that takes an 'args' parameter
def main(args):
    # Make several requests to the same host and reuse the underlying TCP connection
    s = requests.Session()
    
    # Run the test cases
    for test_set in LOOKUP_TEST_SET:
            url = f'http://{args.host}:{args.port}{test_set}'
            print("URL: ",url)
            request_body = url.split('/')
            toy = request_body[4]
            response = requests.get(url)
            if response.status_code == 404:
                 print(f"Sorry {toy} not found")
            print(response.content.decode())

    print('------------------------------------------------')
    time.sleep(3)

    
if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Client.')
    # Add arguments for the port, host, and probability
    parser.add_argument('--port', dest='port', help='Port', default=8087, type=int)
    parser.add_argument('--host', dest='host', help='Host', default='127.0.0.1', type=str)

    # Parse the arguments and store them in a variable called 'args'
    args = parser.parse_args()

    # Call the main function with the 'args' parameter
    main(args)

