"""Helpers to collect and format system metrics for the dashboard."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

import psutil


def _bytes_to_gb(value: float) -> float:
    """Convert bytes to gigabytes using the binary (1024) base."""

    return value / (1024 ** 3)


def _collect_uptime() -> timedelta:
    """Return the system uptime as ``timedelta``.

    ``psutil.boot_time`` returns a POSIX timestamp. Converting this value to a
    ``datetime`` before subtracting prevents the ``TypeError`` that occurs when
    subtracting a float from a ``datetime`` instance.
    """

    boot_ts = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_ts)
    return datetime.now() - boot_time


def get_system_info() -> Dict[str, Any]:
    """Collect CPU, RAM, disk and uptime metrics in a structured dictionary."""

    cpu_percentage = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    ram_percentage = mem.percent
    ram_used_gb = _bytes_to_gb(mem.used)
    ram_total_gb = _bytes_to_gb(mem.total)

    disk = psutil.disk_usage("/")
    disk_percentage = disk.percent
    disk_used_gb = _bytes_to_gb(disk.used)
    disk_total_gb = _bytes_to_gb(disk.total)

    uptime = _collect_uptime()

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
