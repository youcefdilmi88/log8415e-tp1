import boto3


class CreateLoadBalancer:
    def create_load_balancer(name, security_group_id):
        """
        Description: Connects to AWS and creates a load balancer using the existing subnets.

        Parameters:
        - name (string): The name of the load balancer.
        - security_group_id (string): The IDs of the security groups for the load balancer.

        Returns:
        dict: A dict containing an list of created load balancers.
        """

        ec2_client = boto3.client("ec2")
        elb_client = boto3.client("elbv2")
        subnets = []
        ec2_client_subnets = ec2_client.describe_subnets()
        for subnet in ec2_client_subnets["Subnets"]:
            subnets.append(subnet["SubnetId"])
        return elb_client.create_load_balancer(
            Name=name,
            SecurityGroups=[security_group_id],
            IpAddressType="ipv4",
            Subnets=subnets,
        )
