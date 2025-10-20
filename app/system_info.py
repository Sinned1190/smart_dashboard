import psutil
import datetime
def get_system_info():
    cpu_percentage = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    ram_percentage = mem.percent
    ram_used_gb = mem.used / (1024 ** 3)
    ram_total_gb = mem.total / (1024 ** 3)

    disk = psutil.disk_usage('/')
    disk_percentage = disk.percent
    disk_used_gb = disk.used / (1024 ** 3)
    disk_total_gb = disk.total / (1024 ** 3)

    boot_ts = psutil.boot_time()
    uptime = datetime.timedelta(seconds=(datetime.datetime.now() - boot_ts))

    return {
        "cpu_percentage": cpu_percentage,
        "ram_percentage": ram_percentage,
        "ram_used_gb": ram_used_gb,
        "ram_total_gb": ram_total_gb,
        "disk_percentage": disk_percentage,
        "disk_used_gb": disk_used_gb,
        "disk_total_gb": disk_total_gb,
        "uptime": uptime,
    }