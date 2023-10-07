from datetime import date, datetime, timedelta
from metric_data import MetricData
import time
import boto3
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import (DateFormatter)

TARGET_GROUP_CLOUDWATCH_METRICS = ['RequestCountPerTarget']
ELB_CLOUDWATCH_METRICS = ['NewConnectionCount', 'ProcessedBytes', 'TargetResponseTime']
EC2_CLOUDWATCH_METRICS = ['CPUUtilization', 'NetworkIn', 'NetworkOut']

elb_metrics_count = len(ELB_CLOUDWATCH_METRICS)
tg_metrics_count = len(TARGET_GROUP_CLOUDWATCH_METRICS)
ecs_metrics_count = len(EC2_CLOUDWATCH_METRICS)

class CloudWatchMonitor:

    def __init__(self):
        """
        Description: Initializes the CloudWatchMonitor class with a CloudWatch client.
        
        Parameters: None
        
        Returns: None
        """
        self.cw_client = boto3.client('cloudwatch')

    def appendMetricDataQy(self, container, cluster_id, metrics, dimension):
        """
        Description: Appends metric data query to the given container based on the metrics and dimension provided.

        Parameters:
        - container (list): The list to which metric data queries are appended.
        - cluster_id (str): ID of the cluster.
        - metrics (list): List of metric names to append.
        - dimension (dict): The dimension for the metric data.

        Returns: None
        """
        for metric in metrics:
            if metric in EC2_CLOUDWATCH_METRICS:
                namespace = 'AWS/EC2'
            else:
                namespace = 'AWS/ApplicationELB'
            container.append({
                "Id": (metric + dimension["Name"] + cluster_id).lower(),
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric,
                        "Dimensions": [
                            {
                                "Name": dimension["Name"],
                                "Value": dimension["Value"]
                            }
                        ]
                    },
                    "Period": 60,
                    "Stat": "Sum",
                }
            })

    def build_cloudwatch_query(self, instances):
        """
        Description: Builds a CloudWatch query for the provided EC2 instances.

        Parameters:
        - instances (list): List of EC2 instances for which the query should be built.

        Returns:
        list: A list of metric data queries.
        """
        targetgroup_val_1, targetgroup_val_2 = "targetgroup/cluster1", "targetgroup/cluster2"
        loadbal_val = "app/elb"
        response_elb = self.cw_client.list_metrics(Namespace= 'AWS/ApplicationELB', MetricName= 'RequestCount', Dimensions=[
            {
                'Name': 'LoadBalancer',
            },
        ])
        response_tg = self.cw_client.list_metrics(Namespace= 'AWS/ApplicationELB', MetricName= 'RequestCount', Dimensions=[
            {
                'Name': 'TargetGroup',
            },
        ])
        dimension_tg_1 = dimension_tg_2 = dimension_lb = None
        for response in response_elb["Metrics"]:
            dimension = response["Dimensions"][0]
            if loadbal_val in dimension["Value"]:
                dimension_lb = dimension

        for response in response_tg["Metrics"]:
            dimension = response["Dimensions"][0]
            if targetgroup_val_1 in dimension["Value"]:
                dimension_tg_1 = dimension
            elif targetgroup_val_2 in dimension["Value"]:
                dimension_tg_2 = dimension

        metricDataQy = []
        metric_pipeline = [('1', dimension_tg_1, TARGET_GROUP_CLOUDWATCH_METRICS), ('2', dimension_tg_2, TARGET_GROUP_CLOUDWATCH_METRICS),
            ('', dimension_lb, ELB_CLOUDWATCH_METRICS)]
        metric_pipeline += [(instance.id.split('-')[1], { 'Name': 'InstanceId', 'Value': instance.id }, EC2_CLOUDWATCH_METRICS) for instance in instances]
        for metric_action in metric_pipeline:
            self.appendMetricDataQy(metricDataQy, metric_action[0], metric_action[2], metric_action[1])
        return metricDataQy

    def get_data(self, query):
        """
        Description: Queries CloudWatch for metric data based on the provided query.

        Parameters:
        - query (list): A list of metric data queries.

        Returns:
        dict: A dictionary containing the CloudWatch metric data results.
        """
        print('Started querying CloudWatch.')
        return self.cw_client.get_metric_data(
            MetricDataQueries=query,
            StartTime=datetime.utcnow() - timedelta(minutes=30),
            EndTime=datetime.utcnow(),
        )

    def parse_data(self, response):
        """
        Description: Parses the provided CloudWatch metric data response.

        Parameters:
        - response (dict): The CloudWatch metric data response.

        Returns:
        tuple: A tuple containing parsed metric data for target groups, load balancer, and ECS.
        """
        results = response["MetricDataResults"]
        tg_metrics_cluster1 = results[:tg_metrics_count]
        tg_metrics_cluster2 = results[tg_metrics_count:tg_metrics_count * 2]
        elb_metrics = results[tg_metrics_count * 2:tg_metrics_count * 2 + elb_metrics_count]
        ecs_metrics = results[tg_metrics_count * 2 + elb_metrics_count:]

        return tg_metrics_cluster1, tg_metrics_cluster2, elb_metrics, ecs_metrics

    def group_ecs_metrics(self, ecs_metrics):
        """
        Description: Groups ECS metrics by instances.

        Parameters:
        - ecs_metrics (list): A list of ECS metric data results.

        Returns:
        list: A list of grouped ECS metric data results.
        """
        grouped_ecs_metrics = []
        i = 0
        while i < len(ecs_metrics):
            group = []
            for _ in range(len(EC2_CLOUDWATCH_METRICS)):
                group.append(ecs_metrics[i])
                i += 1
            grouped_ecs_metrics.append(group)

        return grouped_ecs_metrics

    def generate_graphs(self, tg_metrics_cluster1, tg_metrics_cluster2, elb_metrics, ecs_metrics):
        """
        Description: Generates graphs for the provided metric data and saves them under 'graphs/' directory.

        Parameters:
        - tg_metrics_cluster1 (list): Metric data for target group cluster 1.
        - tg_metrics_cluster2 (list): Metric data for target group cluster 2.
        - elb_metrics (list): Metric data for the load balancer.
        - ecs_metrics (list): Metric data for ECS.

        Returns: None
        """
        print('Generating graphs under graphs/.')

        self.generate_metric_groups_graphs([tg_metrics_cluster1, tg_metrics_cluster2])
        self.generate_metric_groups_graphs([elb_metrics])
        self.generate_metric_groups_graphs(ecs_metrics, True)

    def generate_metric_groups_graphs(self, metric_groups, bar=False):
        """
        Description: Generates graphs for the provided metric groups.

        Parameters:
        - metric_groups (list): A list of metric groups for which graphs should be generated.
        - bar (bool): Indicates whether the graph should be a bar graph.

        Returns: None
        """
        
        for i in range(len(metric_groups[0])):
            data_groups = [MetricData(group[i]) for group in metric_groups]

            label = data_groups[0].label

            fig, ax = plt.subplots()
            if not bar:
                formatter = DateFormatter("%H:%M:%S")
                ax.xaxis.set_major_formatter(formatter)
                plt.xlabel("Timestamps")
            else:
                plt.xlabel("Instances")

            for data in data_groups:
                if not bar:
                    plt.plot(data.timestamps, data.values, label=getattr(data, "grouplabel", None))
                else:
                    time.sleep(30)
                    if data.values:
                        plt.bar(data.grouplabel, data.values[0])

            if not bar:
                plt.title(label)
            else:
                plt.title("Average " + label)

            if len(data_groups) > 1 and not bar:
                plt.legend(loc='best')

            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.savefig(f"graphs/{label}")
            plt.close()