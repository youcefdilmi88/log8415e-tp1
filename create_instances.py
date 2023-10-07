import boto3


class CreateInstances:
    def create_instances(
        instance_type, count, image_id, key_name, user_data, security_group_name
    ):
        """
        Description: Connects to AWS and creates EC2 instances.

        Parameters:
        - instance_type (string): The type of instance to create (ex. T2.micro).
        - count (type): How many instances to create.
        - image_id (type): AMI ID.
        - key_name (type): Key pair's name, the key pair is a security credential.
        - user_data (type): Data (ex. shell script) to be executed on the instance(s) at launch.
        - security_group_name (type): Security group's name, the security group is a set of firewall rules.

        Returns:
        list(ec2.Instance): A list containing the created instances.
        """
        ec2_resource = boto3.resource("ec2")
        return ec2_resource.create_instances(
            InstanceType=instance_type,
            MinCount=count,
            MaxCount=count,
            ImageId=image_id,
            KeyName=key_name,
            UserData=user_data,
            SecurityGroups=[security_group_name],
        )
