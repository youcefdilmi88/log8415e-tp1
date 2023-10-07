import boto3


class CreateSecurityGroup:
    def create_security_group(name):
        """
        Description: Connects to AWS and creates a security group using the existing VPC. The security group allows all HTTP (port80) and SSH traffic (port 22).

        Parameters:
        - name (string): The name of the security group.

        Returns:
        EC2.SecurityGroup: An object representing the created security group.
        """

        ec2_client = boto3.client("ec2")
        ec2_resource = boto3.resource("ec2")
        response_vpcs = ec2_client.describe_vpcs()
        vpc_id = response_vpcs.get("Vpcs", [{}])[0].get("VpcId", "")

        response_security_group = ec2_client.create_security_group(
            GroupName=name, Description="Security group for our instances", VpcId=vpc_id
        )

        security_group_id = response_security_group["GroupId"]

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 80,
                    "ToPort": 80,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                },
            ],
        )

        return ec2_resource.SecurityGroup(response_security_group["GroupId"])
