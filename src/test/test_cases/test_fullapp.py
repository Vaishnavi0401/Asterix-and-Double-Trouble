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
    "/product/Train"
    ]

# 1) Buy 1 quantity of Fox, 2) Buy 10 quantity of Tux 3) Buy 22 quantity of Barbie
# Do this 100 times
# All the requests should be processed successfully
ORDER_TEST_SET1 = [
    "/orders/Fox/1",
    "/orders/Tux/10",
    "/orders/Barbie/22"
]

# Buy more than available quantity 
# Buy 1 quantity each stock 
# Do it 101 times
ORDER_TEST_SET2 = [
    "/orders/Tux/2000",
    "/orders/Fox/1000",
    "/orders/Marbles/2200",
    "/orders/Barbie/3000",
    "/orders/Elephant/11100",
    "/orders/Legos/1500"
]

#Get order details from order number
ORDER_TEST_SET3 = [
    "/orders/2",
    "/orders/3",
    "/orders/1000",
    "/orders/400"
]
# Invalid URL
# Place an order with negative quantity -> error 400, invalid quantity
# Place an order with 0 quantity -> error 400, invalid quantity
# Place an order with invalid url
ORDER_TEST_SET4 = [
    "/orders/Tux/-10",
    "/orders/Tux/0"
]

# Define the main function that takes an 'args' parameter
def main(args):
    # Make several requests to the same host and reuse the underlying TCP connection
    s = requests.Session()
    
    # Run the test cases
    for test_set in [LOOKUP_TEST_SET, ORDER_TEST_SET1, ORDER_TEST_SET3, ORDER_TEST_SET2, ORDER_TEST_SET4]:
        for request in test_set:
            url = f'http://{args.host}:{args.port}{request}'
            print("URL: ",url)
            if request.startswith("/product") or (request.startswith("/orders") and request.count("/") == 2):
                response = requests.get(url)
            else:
                print(url)
                request_body = url.split('/')
                toy_name = request_body[4]
                quantity = request_body[5]     
                request_body = {"name": toy_name, "quantity": quantity}  
                request_body_json = json.dumps(request_body)             
                response = requests.post(url, data=request_body_json)
                if response.status_code == 200:
                    print(response.content.decode())
                elif response.status_code == 400:
                    print(f"Sorry {toy_name} is out of stock or invalid quantity")
                else:
                    print(response.content.decode())
  
            print(response.content.decode())

        print('------------------------------------------------')
        time.sleep(3)


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Client.')
    # Add arguments for the port, host, and probability
    parser.add_argument('--port', dest='port', help='Port', default=8080, type=int)
    parser.add_argument('--host', dest='host', help='Host', default='127.0.0.1', type=str)

    # Parse the arguments and store them in a variable called 'args'
    args = parser.parse_args()

    # Call the main function with the 'args' parameter
    main(args)