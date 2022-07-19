import docker
from utils.stats import get_CPU_percent
import time
import datetime
import csv
import os 
import argparse

parser = argparse.ArgumentParser(description='Container monitor.')
parser.add_argument("-cid", "--container-id", required=True, 
                    help="Container ID to monitor.", type=str)

parser.add_argument("-t", "--time", required=False,
                    help="Monitoring time [seconds]. If not set (or 0 is setted), program will "\
                         "log data until it is interrumpted.", type=int, default=0)

args = vars(parser.parse_args())


folder = "outputs"
container_id = args["container_id"]
max_time = args["time"]

client = docker.from_env()
container = client.containers.get(container_id)
status = container.stats(decode=True, stream = True)

prev_cpu = None
start_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
start_time = time.time()
filename = f"log_{container_id}_{start_datetime}.csv"
os.makedirs(folder, exist_ok=True)

with open(os.path.join(folder, filename), "w") as file:
    writter = csv.DictWriter(file, ["cpu_percentage", "mem_used_mb"])
    writter.writeheader()
    for measure in status:
        current_cpu = measure["cpu_stats"]
        current_memory = (
            measure["memory_stats"]["usage"] -
            measure["memory_stats"]["stats"]["cache"] +
            measure["memory_stats"]["stats"]["active_file"]
            ) / (1024 ** 2)

        cpu_percentage = get_CPU_percent(prev_cpu, current_cpu)
        prev_cpu = current_cpu
        info = {
            "cpu_percentage": round(cpu_percentage, 2),
            "mem_used_mb": round(current_memory, 2)
            }
        writter.writerow(info)
        if (time.time() - start_time) >= max_time:
            break

