from datetime import date, datetime
from workloads import run_workloads
from cloudwatch import CloudWatchMonitor
from create_security_group import CreateSecurityGroup
from create_instances import CreateInstances
from create_load_balancer import CreateLoadBalancer
from create_target_group import CreateTargetGroup
from register_targets import RegisterTargets
from create_listener import CreateListener
from create_path_forward_rule import CreatePathForwardRule
import time
import json

from matplotlib.dates import DateFormatter


import json
from datetime import datetime, date


def json_serial(obj):
    """
    Description: This code verifies if obj is an instance of either the datetime or date class. If obj is an instance of datetime or date, the code will return its string representation in ISO format.

    Parameters:
    - obj (object): The object to serialize.

    Returns:
    str: A serialized string for the object, or raises a TypeError if not serializable.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def print_response(response):
    """
    Description: Saves the provided response object to a JSON file.

    Parameters:
    - response (object): The response object to save to a JSON file.

    Returns:
    None: The function only prints and saves data without returning any value.
    """
    print("Saving query result in graphs/response.json.")
    with open("graphs/response.json", "w") as data_file:
        json.dump(response, data_file, indent=4, sort_keys=True, default=json_serial)


# PROGRAM EXECUTION

# 1. Generate infrastructure (EC2 instances, load balancers and target groups)
print("Creating security group...")
security_group = CreateSecurityGroup.create_security_group("sg")
print("security group created!")

print("Creating load balancer...")
elb = CreateLoadBalancer.create_load_balancer("elb", security_group.id)
print("load balancer created!")

user_data_cluster1 = open("flask_cluster1.sh", "r").read()
user_data_cluster2 = open("flask_cluster2.sh", "r").read()

print("Creating clusters...")
m4_Instances = CreateInstances.create_instances(
    "m4.large",
    5,
    "ami-08c40ec9ead489470",
    "vockey",
    user_data_cluster1,
    security_group.group_name,
)
t2_Instances = CreateInstances.create_instances(
    "t2.large",
    4,
    "ami-08c40ec9ead489470",
    "vockey",
    user_data_cluster2,
    security_group.group_name,
)
print("Clusters created!")

# create target groups
print("Creating target groups...")
cluster1_tg = CreateTargetGroup.create_target_group("cluster1")
cluster2_tg = CreateTargetGroup.create_target_group("cluster2")
print("Target groups created!")

# Register targets
print("Registering Instances to target groups...")
RegisterTargets.register_targets(cluster1_tg, m4_Instances)
RegisterTargets.register_targets(cluster2_tg, t2_Instances)
print("Instances registration complete!")

# Create listeners
listener = CreateListener.create_listener(cluster1_tg, elb)

# Create path forward rules
listener_rule_1 = CreatePathForwardRule.create_path_forward_rule(
    cluster1_tg, listener, "/cluster1", 1
)
listener_rule_2 = CreatePathForwardRule.create_path_forward_rule(
    cluster2_tg, listener, "/cluster2", 2
)

print("Finished initializing infrastructure!")
print("Waiting 400 seconds for infra to be ready...")
time.sleep(400)

# 2. Run workloads
run_workloads(elb)

# 3. Build query to collect desired metrics from the last 30 minutes (estimated max workload time)
cloudwatch_monitor = CloudWatchMonitor()
query = cloudwatch_monitor.build_cloudwatch_query(m4_Instances + t2_Instances)

# 4. Query CloudWatch client using built query
response = cloudwatch_monitor.get_data(query)

# 5. Parse MetricDataResults and store metrics
(
    tg_metrics_cluster1,
    tg_metrics_cluster2,
    elb_metrics,
    ecs_metrics,
) = cloudwatch_monitor.parse_data(response)
ecs_metrics = cloudwatch_monitor.group_ecs_metrics(ecs_metrics)

# 6. Generate graphs and save under /metrics folder
cloudwatch_monitor.generate_graphs(
    tg_metrics_cluster1, tg_metrics_cluster2, elb_metrics, ecs_metrics
)

print("Charts created successfully")
