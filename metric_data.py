class MetricData:
    def __init__(self, metric):
        label = metric["Label"]

        if "cluster" in label:
            self.grouplabel = label.split("/")[2]
            label = label.split(" ")
            label = label.pop()
        elif "AWS/ApplicationELB" in label:
            label = "ApplicationELB-" + label.split(" ").pop()
        else:
            self.grouplabel = label.split(" ")[1]
            label = "EC2-" + label.split(" ").pop()

        self.label = label
        self.timestamps = metric["Timestamps"]
        self.values = metric["Values"]
