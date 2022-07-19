
def get_CPU_percent(prevCPU, currentCPU):
    cpuPercent = 0.0
    if prevCPU is None: return cpuPercent
    cpuDelta = currentCPU["cpu_usage"]["total_usage"] - prevCPU["cpu_usage"]["total_usage"]
    systemDelta = currentCPU["system_cpu_usage"] - prevCPU["system_cpu_usage"]

    if systemDelta > 0.0 and cpuDelta > 0.0:
        cpuPercent = (cpuDelta / systemDelta) * len(currentCPU["cpu_usage"]["percpu_usage"]) * 100.0
    return cpuPercent
    
    