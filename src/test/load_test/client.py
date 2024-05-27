# Import necessary libraries
import requests
import random
import time
from dotenv import load_dotenv
import os
import json
import argparse

# Load environment variables from .env file
load_dotenv()

# Define a class for the ToyStoreClient
class ToyStoreClient:
    @staticmethod
    def run_session(total_query_time, total_buy_time, order_cnt,lookup_cnt, order_history):
        # Select a random product name from the list
        product_name = random.choice(TOY_NAME_LIST)
        print("Query TOY:", product_name)

        # Construct the URL to query the product information
        base_url = f"http://{host}:{port}"
        url = f"{base_url}/product/{product_name}"
        print("Toy URL:", url)

        response = None
        while response is None:
            try:
                # Measure the start time of the query
                query_start_time = time.time()
                # Send a GET request to retrieve product information
                response = session.get(url)
                # Measure the end time of the query and calculate the time taken
                query_end_time = time.time()
                diff_query_time = query_end_time - query_start_time
            except: 
                continue    

        lookup_cnt += 1
        total_query_time += diff_query_time

        print("Toy Lookup Response: ",response.json())

        # Handle the response based on the status code
        if response.status_code == 200:
            data = response.json()
            nested_data = data.get("data")
            quantity = nested_data.get("quantity")
            prob = random.uniform(0, prob_val)
            quant = random.choice(ORDER_LIST)

            # If the quantity is available and a random condition is met, place an order
            if quantity > 0 and random.random() <= prob:
                request_body = {"name": product_name, "quantity": quant}
                print("Order request:", request_body)

                # Convert the request body to JSON format
                request_body_json = json.dumps(request_body)

                # Construct the URL to place an order
                url = f"{base_url}/orders"
                response = None
                while response is None:
                    try:
                        post_start_time = time.time()
                        response = session.post(url, data=request_body_json)
                        post_end_time = time.time()
                        diff_post_time = post_end_time - post_start_time
                    except: 
                        continue

                order_cnt += 1
                total_buy_time += diff_post_time

                print("Buy Request Response: ", response.json())

                if response.status_code == 200:
                    nested = response.json().get("data")
                    order_number = nested.get("order_number")
                    order_history[order_number] = {"Toy Name": product_name, "Quantity": quant}

        return total_query_time, total_buy_time, order_cnt, lookup_cnt, 

# Main entry point of the script
if __name__ == "__main__":
    # Load environment variables for host and port
    host = os.getenv("host")
    # host = 'ec2-3-89-129-65.compute-1.amazonaws.com'
    port = os.getenv("frontend_port")  # the host and port of the frontend server

    # Create a session for making HTTP requests
    session = requests.Session()

    # Initialize variables to track total query time and total buy time
    total_query_time = 0
    total_buy_time = 0
    lookup_cnt = 0
    order_cnt = 0

    # Define lists of toy names and order quantities
    TOY_NAME_LIST = ["Tux","Dolphin","Whale","Monopoly","Fox","Elephant","Marbles","Lego","Marbles","Python","Pen","Barbie"]
    ORDER_LIST = [4,5,1,20,11,10,22,9,29,19,39,5,6,15,8,7]

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--prob', type=str, help='Probability')
    args = parser.parse_args()
    prob_val = float(args.prob)
    
    order_history={}

    # Run the session multiple times
    for r in range(500):
        print("\n")
        print("Request:", r)
        time.sleep(1)  # Wait for 1 second before each session
        total_query_time, total_buy_time, order_cnt,lookup_cnt  = ToyStoreClient.run_session(
            total_query_time, total_buy_time, order_cnt, lookup_cnt, order_history
        )

   
    # Retrieve order details from the server using order numbers stored in history
    for order_number in order_history.keys():
        base_url = f"http://{host}:{port}"
        url = f"{base_url}/orders/{order_number}"
        response = session.get(url)
        if response.status_code == 200:
            nested = response.json().get("data")
            toy_name = nested.get("Toy name")
            quantity = nested.get("Quantity")
            if toy_name != order_history[order_number]["Toy Name"] or quantity != order_history[order_number]["Quantity"]:
                print("Local database is inconsistent with the order server database - ",order_history[order_number], print(response.json()))
            

    # Print total query time and total buy time
    print("Total lookup request: ",lookup_cnt)
    print("Average lookup request latency:", total_query_time/lookup_cnt)
    if order_cnt != 0:
        print("Total order request: ",order_cnt)
        print("Average order request latency:", total_buy_time/order_cnt)
