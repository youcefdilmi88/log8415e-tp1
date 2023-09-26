import boto3
import env

# look at the README file to setup before running script

session = boto3.Session(
    aws_access_key_id=env.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
    aws_session_token=env.AWS_SESSION_TOKEN,
)

ec2 = session.client("ec2", region_name="us-east-1")

with open("./user_data_script.sh", "r") as f:
    user_data_script = f.read()

instance_params = {
    "ImageId": "ami-0261755bbcb8c4a84",  # Canonical, Ubuntu, 20.04 LTS, amd64 focal image build on 2023-05-17
    "InstanceType": "t2.large",
    "MinCount": 5,  # how many instances are created
    "MaxCount": 5,  # how many instances are created
    "UserData": user_data_script,
    "SecurityGroupIds": ["sg-0766a7c00bada6d8a"],
}

# creates ec2 instance using parameters above
response = ec2.run_instances(**instance_params)


for i in range(5):
    instance_id = response["Instances"][i]["InstanceId"]
    print("New instance ID:", instance_id)  # prints the id of each ec2 instance created
