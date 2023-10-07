import requests
import time
import threading


def call_endpoint_http(elb_dns, route):
    """
    Description: Builds a request to call the specified cluster and then initiates the request.

    Parameters:
    - elb_dns (string): The DNS name of the load balancer.
    - route (string): The route of the cluster to call.

    Returns:
    requests.Response: The response object to the HTTP call.
    """

    headers = {"content-type": "application/json"}
    url = f"http://{elb_dns}{route}"

    try:
        response = requests.get(url, headers=headers, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Error encountered while making the HTTP request to {url}: {e}")
        return None


def run_first_workload(elb_dns):
    """
    Description: Sends 1000 GET requests sequentially to cluster1.

    Parameters:
    - elb_dns (string): The DNS name of the load balancer.

    Returns:
    void
    """

    print("Started first workload.")
    for _ in range(1000):
        call_endpoint_http(elb_dns, "/cluster1")
    print("Finished first workload.")


def run_second_workload(elb_dns):
    """
    Description: Sends 500 GET requests to cluster2, then one minute sleep, followed by 1000 GET requests to cluster2.

    Parameters:
    - elb_dns (string): The DNS name of the load balancer.

    Returns:
    void
    """

    print("Started second workload.")
    for _ in range(500):
        call_endpoint_http(elb_dns, "/cluster2")
    time.sleep(60)

    for _ in range(1000):
        call_endpoint_http(elb_dns, "/cluster2")
    print("Finished second workload.")


def run_workloads(elb):
    """
    Description: Initiates 2 thread, one for each workload.

    Parameters:
    - elb (dict): A dict containing an list of load balancers. This is the load balancer that will listen for HTTP requests. Used to get the DNS name of the load balancer.

    Returns:
    void
    """

    elb_dns = elb["LoadBalancers"][0]["DNSName"]

    first_workload_thread = threading.Thread(target=run_first_workload, args=[elb_dns])
    second_workload_thread = threading.Thread(
        target=run_second_workload, args=[elb_dns]
    )

    first_workload_thread.start()
    second_workload_thread.start()

    first_workload_thread.join()
    second_workload_thread.join()
