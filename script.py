import boto3
import constant


import boto3

# look at the README file to setup before running script

session = boto3.Session(
    aws_access_key_id=constant.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=constant.AWS_SECRET_ACCESS_KEY,
    aws_session_token=constant.AWS_SESSION_TOKEN,
)

ec2 = session.client("ec2", region_name="us-east-1")

instance_params = {
    "ImageId": "ami-03a6eaae9938c858c",  # found when done manually with aws UI
    "InstanceType": "t2.micro",
    "MinCount": 5,  # how many instance is created
    "MaxCount": 5,
}


response = ec2.run_instances(
    **instance_params
)  # creates ec2 instance using parameters above


for i in range(5):
    instance_id = response["Instances"][i]["InstanceId"]
    print("New instance ID:", instance_id)  # prints the id of each ec2 instance created
