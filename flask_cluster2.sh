#!/bin/bash

# Installs Flask
# Creates a Flask app that returns the instance ID
# Route to the app: http://<public_ip>/cluster2
# Runs the Flask app on port 80
# Uses ec2metadata to get the instance ID
# Uses tee to write the Flask app to a file

apt-get update
apt-get -y install python3-pip 
pip3 install flask
mkdir flask_app 
cd flask_app
instance_id=$(ec2metadata --instance-id) 
echo "from flask import Flask
app = Flask(__name__)
@app.route('/cluster2')
def myFlaskApp():

        return \""$instance_id" is responding now! \"

if __name__ == \"__main__\":
       app.run(host='0.0.0.0', port=80) " | tee app.py
python3 app.py 