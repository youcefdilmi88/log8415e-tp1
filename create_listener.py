import boto3


class CreateListener:
    def create_listener(tg_cluster, load_balancer):
        """
        Description: Connects to AWS and creates a listener for the load balancer. This code sets up a listener on a Load Balancer that listens for HTTP requests on port 80 and forwards them to a specified target group (tg_cluster).

        Parameters:
        - tg_cluster (dict): A dict containing an list of target groups. This is the target group that will receive the HTTP requests.
        - load_balancer (dict): A dict containing an list of load balancers. This is the load balancer that will listen for HTTP requests.

        Returns:
        dict: A dict containing an list of created listeners.
        """

        elb_client = boto3.client("elbv2")
        return elb_client.create_listener(
            DefaultActions=[
                {
                    "TargetGroupArn": tg_cluster["TargetGroups"][0]["TargetGroupArn"],
                    "Type": "forward",
                },
            ],
            LoadBalancerArn=load_balancer["LoadBalancers"][0]["LoadBalancerArn"],
            Port=80,
            Protocol="HTTP",
        )
