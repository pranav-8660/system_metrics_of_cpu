import psutil as pu
import time
from fastapi import FastAPI

app = FastAPI()

def getCpuUsageParams():
    cpu_usage = pu.cpu_percent(interval=1)
    cpu_load_average = pu.getloadavg()
    cpu_frequency = pu.cpu_freq().current
    cpu_core_utilization = pu.cpu_percent(interval=1,percpu=True)

    cpu_usage_params = {
    "CPU-USAGE":cpu_usage,"CPU_LOAD_AVERAGE":cpu_load_average,"CPU_FREQUENCY":cpu_frequency,"CPU_CORE_UTILIZATION":cpu_core_utilization
    }

    return cpu_usage_params

def getMemoryMetrics():

    virtual_memory = pu.virtual_memory()
    swap_memory = pu.swap_memory()

    total_memory= virtual_memory.total // (1024 ** 3)
    used_memory= virtual_memory.used // (1024 ** 3)
    free_memory= virtual_memory.available // (1024 ** 3)
    swap_memory_usage=swap_memory.used // (1024 ** 3)

    memory_usage_metrics = {
        "total_memory_gb":total_memory, "used_memory_gb":used_memory, "free_memory_gb":free_memory, "swap_memory_usage_gb":swap_memory_usage
    }

    return memory_usage_metrics

def getDiskMetrics():

    disk_usage = pu.disk_usage("/")

    total_disk_gb = round(disk_usage.total // (1024 ** 3),2)
    disk_usage_gb = round(disk_usage.used // (1024 ** 3),2)
    free_disk_gb = round(disk_usage.free // (1024**3),2)
    disk_usage_percent= disk_usage.percent

    disk_usage_metrics = {
        "total_disk_gb":total_disk_gb,"disk_usage_gb":disk_usage_gb,"free_disk_gb":free_disk_gb,"disk_usage_percent":disk_usage_percent
    }
    return disk_usage_metrics 

def processAndsystemMetrics():
    running_processes_count = len(pu.pids())
    system_uptime_hours = (time.time() - pu.boot_time()) // 3600
    logged_in_users = [user.name for user in pu.users()]

    process_system_metrics = {
        "running_processes_count":running_processes_count, "system_uptime_hours":system_uptime_hours, "logged_in_users":logged_in_users
    }

    return process_system_metrics

def getNetworkMetrics():
    net_io = pu.net_io_counters()

    bytes_sent = net_io.bytes_sent // (1024 ** 2)
    bytes_recieved = net_io.bytes_recv // (1024 ** 2)
    packets_sent = net_io.packets_sent 
    packets_recieved = net_io.packets_recv 
    error_in = net_io.errin
    error_out = net_io.errout
    
    network_metrics = {
        "bytes_sent_mb":bytes_sent,"bytes_recieved_mb":bytes_recieved,"packets_sent":packets_sent,
        "packets_recieved":packets_recieved,"error_in":error_in,"error_out":error_out
    }
    return network_metrics

@app.get("/disk/")
def disk_usage():
    return getDiskMetrics()

@app.get("/cpu/")
def cpu_usage():
    return getCpuUsageParams()

@app.get("/processnsystems/")
def process_systems():
    return processAndsystemMetrics()


@app.get("/memory/")
def memory_usage():
    return getMemoryMetrics()

@app.get("/all/")
def all_cpu_metrics():
    all_met = {
        "DISK_USAGE_METRICS":getDiskMetrics(),"PROCESS_AND_SYSTEM_METRICS":processAndsystemMetrics(),
        "CPU_USAGE_METRICS":getCpuUsageParams(),"MEMORY_USAGE_METRICS":getMemoryMetrics(),"TEMPERATURE":pu.sensors_temperatures(),"NETWORK_METRICS":getNetworkMetrics()
    }
    return all_met
