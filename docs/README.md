# How to start the services on local

### Change the environment variables in .env if necessary.

1. Open a terminal and run catalog.py to start the catalog service. 
```shell
cd ${LAB3_PATH}/src/Catalog
```
```python
python3 catalog.py 
```

2. Open another terminal to start the order service.
```shell
cd ${LAB3_PATH}/src/Order
```
```shell
chmod +x run-replicas.sh
./run-replicas.sh
```

3. Open the third terminal to start the frontend service
```shell
cd ${LAB2_PATH}/src/Frontend-Service
```
```python
python3 frontend-service.py 
```

4. After starting the three services, a client can start sending requests via the port that the frontend is listening to.
```shell
cd ${LAB3_PATH}/src/client
```
```python
python3 client.py 
```

5. Or, run multiple clients concurrently:
```shell
chmod +x client5.sh
```
```shell
./client5.sh
```

# How to start the services on AWS

### Change the environment variables in .env if necessary.

1.  First we created an `t2.micro` EC2 instance in the `us-east-1` region on AWS 
```shell
$ aws ec2 run-instances --image-id ami-0d73480446600f555 --instance-type t2.micro --key-name vockey > instance.json
```

2.   Checking status of our instance to find the public DNS name
```shell
aws ec2 describe-instances --instance-id ec2-44-223-61-2.compute-1.amazonaws.com
```

3.  Access the instance via ssh
```shell
chmod 400 labuser.pem
#for our frontend service, which uses port=477
aws ec2 authorize-security-group-ingress --group-name default --protocol tcp --port 4773 --cidr 0.0.0.0/0
ssh -i labsuser.pem ubuntu@ec2-44-223-61-2.compute-1.amazonaws.com
```

4. Inside the instance, install the required packages:
```shell
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install python3-pip
pip3 install requests
pip3 install python-dotenv
pip3 install pandas
```

5. Cloning our repo on the instance
```shell
Git clone https://github.com/umass-cs677-current/spring24-lab3-Gargeeshah-vaishnavi0401.git
cd /spring24-lab3-Gargeeshah-vaishnavi0401/src 
```

6. Running all the five services
```shell
chmod +x run-all.sh
./run-all.sh 
```

7. Run concurrent clients locally
```shell
cd ${LAB3_PATH}/src/test/load_test
```
```shell
chmod +x client5.sh
./client5.sh 
```
