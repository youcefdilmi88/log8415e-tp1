# # LOG8415 - LAB1 - Fall 2023

# Public repository: git@github.com:youcefdilmi88/log8415e-tp1.git

# dependencies to run

- install Docker Engine

# to run script

- fill in the .aws_creds file with your AWS CLI credentials
- chmod +x run.sh
- ./run.sh

# Authors

- Youcef Anis Dilmi
- Victor Kim
- Yasser Benmansour
- Mohammed Ridha Ghoul

# Description

This application creates an infrastructure that includes an Application Load Balancer as well as two target groups (clusters). Cluster 1 consists of 5 EC2 M4.large instances, and Cluster 2 has 4 EC2 T2.large instances. We created a listener associated with the load balancer to redirect traffic to the appropriate cluster based on the route used by the client in their request. After setting up this infrastructure, we applied workloads to the load balancer and monitored the insfrastructure's performance, which we then presented in the form of graphs.

The application is built with Python and runs inside a docker container.
