import boto3
from create_target_group import CreateTargetGroup


class RegisterTargets:
    def register_targets(target_group, instances):
        """
        Description: Connects to AWS and binds target instances to a specific target group.

        Parameters:
        - target_group (dict): A dict containing an list of target groups. This is the target group that will receive the HTTP requests.
        - instances (list(ec2.Instance)): A list of EC2 instances that will populate the target group (cluster).

        Returns:
        dict: A dict containing metadata about the operation.
        """

        elb_client = boto3.client("elbv2")
        targets = CreateTargetGroup.get_targets(instances)

        for instance in instances:
            instance.wait_until_running()

        return elb_client.register_targets(
            TargetGroupArn=target_group["TargetGroups"][0]["TargetGroupArn"],
            Targets=targets,
        )
