# This file create a docker image with all the necessary dependencies to run the application. This Dockerfile is based on an image that already has Python installed. It also copies all the files needed to run the application in the container. Finally, it runs the main.py file when the container is started.


FROM python:3

RUN mkdir -p metrics/

RUN mkdir -p graphs/

RUN pip install boto3 requests matplotlib python-dotenv

COPY .aws_creds /

COPY main.py /

COPY create_security_group.py /

COPY create_instances.py /

COPY create_load_balancer.py /

COPY metric_data.py /

COPY cloudwatch.py /

COPY create_target_group.py / 

COPY register_targets.py / 

COPY create_listener.py / 

COPY create_path_forward_rule.py / 

COPY workloads.py /

COPY flask_cluster1.sh / 

COPY flask_cluster2.sh /

CMD [ "python", "./main.py" ]
