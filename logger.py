import docker
from utils.stats import get_CPU_percent
import time
import datetime
import csv
import os 
import argparse
from plotter import Plotter

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Container monitor.')
    parser.add_argument("-cid", "--container-id", required=True, 
                        help="Container ID to monitor.", type=str)

    parser.add_argument("-t", "--time", required=False,
                        help="Monitoring time [seconds]. If not set (or 0 is setted), program will "\
                            "log data until it is interrumpted.", type=int, default=0)

    parser.add_argument("-p", "--plot", required=False,
                        help="If set, plot will be saved.",
                        default=False, action='store_true')

    args = vars(parser.parse_args())


    folder = "outputs"
    plots_folder = "plots"
    container_id = args["container_id"]
    max_time = args["time"]
    plot_bool = args["plot"]

    client = docker.from_env()
    container = client.containers.get(container_id)
    status = container.stats(decode=True, stream = True)

    prev_cpu = None
    start_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H_%M_%S")
    start_time = time.time()
    filename = f"log_{container_id}_{start_datetime}.csv"
    os.makedirs(folder, exist_ok=True)
    os.makedirs(plots_folder, exist_ok=True)

    with open(os.path.join(folder, filename), "w") as file:
        writter = csv.DictWriter(file, ["time", "datetime", "cpu_percentage", "mem_used_mb"])
        writter.writeheader()
        for measure in status:
            time_now = time.time()
            datetime_now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H_%M_%S")
            current_cpu = measure["cpu_stats"]
            current_memory = (
                measure["memory_stats"]["usage"] -
                measure["memory_stats"]["stats"]["total_inactive_file"]
                ) / (1024 ** 2)
            cpu_percentage = get_CPU_percent(prev_cpu, current_cpu)
            prev_cpu = current_cpu
            info = {
                "time": int(time_now - start_time),
                "datetime": datetime_now,
                "cpu_percentage": round(cpu_percentage, 2),
                "mem_used_mb": round(current_memory, 2)
                }
            writter.writerow(info)
            if (time_now - start_time) >= max_time:
                break

    if plot_bool:
        Plotter(plots_folder, os.path.join(folder, filename))