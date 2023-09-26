#!/bin/bash

# Update and install necessary software
apt update
apt install -y python3-pip
pip3 install flask requests

# Create the Flask app
cat <<EOT >> /home/ubuntu/app.py
import requests
from flask import Flask

app = Flask(__name__)

def get_instance_id():
    try:
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id", timeout=1
        )
        return response.text
    except requests.RequestException:
        return "unknown"


@app.route("/")
def hello():
    instance_id = get_instance_id()
    print(f"Instance {instance_id} is responding now!)
    return f"Instance {instance_id} is responding now!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
EOT

# Start the Flask app
sudo nohup python3 /home/ubuntu/app.py &
