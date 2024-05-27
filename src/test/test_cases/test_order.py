import requests
import argparse
import http.client
import sys
import json
import random
import time
import itertools


# 1) Buy 1 quantity of Fox, 2) Buy 10 quantity of Tux 3) Buy 22 quantity of Barbie
# Do this 100 times
# All the requests should be processed successfully
operation = [
    "/orders/Fox/1",
    "/orders/Tux/10",
    "/orders/Barbie/22"
]
ORDER_TEST_SET1 = [operation for i in range(3)]
ORDER_TEST_SET1 = list(itertools.chain.from_iterable(ORDER_TEST_SET1))


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
    "/orders/Tux/0",
    "/order/Tux/10"
]


# Define the main function that takes an 'args' parameter
def main(args):
    # Make several requests to the same host and reuse the underlying TCP connection
    s = requests.Session()
    
    # Run the test cases
    for test_set in [ORDER_TEST_SET1, ORDER_TEST_SET2,ORDER_TEST_SET3, ORDER_TEST_SET4]:
        for request in test_set:
            url = f'http://{args.host}:{args.port}{request}'
            print("URL: ",url)
            if(request.count("/") == 2):
                response = requests.get(url)
                request_body = url.split('/')
                ordern = request_body[4]
                if response.status_code == 200:
                    print(response.content.decode())
                elif response.status_code == 400:
                    print(f"Sorry order number - {ordern} doesn't exists")
                else:
                    print(response.content.decode())
            else:
                request_body = url.split('/')
                toy_name = request_body[4]
                quantity = request_body[5]
                request_body = {"name": toy_name, "quantity": quantity}
                response = requests.post(url, data=request_body)
                if response.status_code == 200:
                    print(response.content.decode())
                elif response.status_code == 400:
                    print(f"Sorry {toy_name} is out of stock or invalid quantity")
                else:
                    print(response.content.decode())
        
        print('------------------------------------------------')
        time.sleep(3)  

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Client.')
    # Add arguments for the port, host, and probability
    parser.add_argument('--port', dest='port', help='Port', default=16008, type=int)
    parser.add_argument('--host', dest='host', help='Host', default='127.0.0.1', type=str)

    # Parse the arguments and store them in a variable called 'args'
    args = parser.parse_args()

    # Call the main function with the 'args' parameter
    main(args)