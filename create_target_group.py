import boto3


class CreateTargetGroup:
    def create_target_group(name):
        """
        Description: Connects to AWS and creates a target group to be targeted by the load balancer in the existing Virtual private network (VPC). The target group is set to receive HTTP requests on port 80.

        Parameters:
        - name (string): The name of the target group.

        Returns:
        dict: A dict containing an list of created target groups.
        """

        ec2_client = boto3.client("ec2")
        elb_client = boto3.client("elbv2")
        vpcs = ec2_client.describe_vpcs()
        vpc_id = vpcs.get("Vpcs", [{}])[0].get("VpcId", "")

        return elb_client.create_target_group(
            Name=name, Protocol="HTTP", Port=80, VpcId=vpc_id
        )

    def get_targets(target_instances):
        """
        Description: This function takes a list of EC2 instances creates a list of IDs from it.

        Parameters:
        - target_instances (list(ec2.Instance)): A list of EC2 instances.

        Returns:
        list(dict): A list of instances IDs
        """

        targets = []
        for instance in target_instances:
            targets.append({"Id": instance.id})
        return targets
