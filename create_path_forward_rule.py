import boto3


class CreatePathForwardRule:
    def create_path_forward_rule(tg_cluster, listener, route, priority):
        """
        Description: Connects to AWS and sets up a forward rule for the specified listener. The listener listens on port 80 and forwards the requests to the specified target group depending on the provided route.

        Parameters:
        - tg_cluster (dict): A dict containing an list of target groups. This is the target group that will receive the HTTP requests.
        - listener (string): A dict containing an list of listeners. This is the listener that will listen for HTTP requests.
        - route (string): The route that will be forwarded to the target group.
        - priority (int): The priority of the rule.

        Returns:
        dict: A dict containing an list of created rules.
        """

        elb_client = boto3.client("elbv2")
        return elb_client.create_rule(
            ListenerArn=listener["Listeners"][0]["ListenerArn"],
            Conditions=[{"Field": "path-pattern", "Values": [route]}],
            Priority=priority,
            Actions=[
                {
                    "Type": "forward",
                    "ForwardConfig": {
                        "TargetGroups": [
                            {
                                "TargetGroupArn": tg_cluster["TargetGroups"][0][
                                    "TargetGroupArn"
                                ],
                                "Weight": 1,
                            },
                        ],
                        "TargetGroupStickinessConfig": {
                            "Enabled": False,
                            "DurationSeconds": 1,
                        },
                    },
                }
            ],
        )
