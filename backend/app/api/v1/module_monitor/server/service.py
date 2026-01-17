import platform
import socket
import time
from pathlib import Path

import psutil

from app.utils.common_util import bytes2human

from .schema import (
    CpuInfoSchema,
    DiskInfoSchema,
    MemoryInfoSchema,
    PyInfoSchema,
    ServerMonitorSchema,
    SysInfoSchema,
)


class ServerService:
    """服务监控模块服务层"""

    @classmethod
    async def get_server_monitor_info_service(cls) -> dict:
        """
        获取服务器监控信息

        返回:
        - Dict: 包含服务器监控信息的字典。
        """
        return ServerMonitorSchema(
            cpu=cls._get_cpu_info(),
            mem=cls._get_memory_info(),
            sys=cls._get_system_info(),
            py=cls._get_python_info(),
            disks=cls._get_disk_info(),
        ).model_dump()

    @classmethod
    def _get_cpu_info(cls) -> CpuInfoSchema:
        """
        获取CPU信息

        返回:
        - CpuInfoSchema: CPU信息模型。
        """
        cpu_times = psutil.cpu_times_percent()
        cpu_num = psutil.cpu_count(logical=True)
        if not cpu_num:
            cpu_num = 1
        return CpuInfoSchema(
            cpu_num=cpu_num,
            used=cpu_times.user,
            sys=cpu_times.system,
            free=cpu_times.idle,
        )

    @classmethod
    def _get_memory_info(cls) -> MemoryInfoSchema:
        """
        获取内存信息

        返回:
        - MemoryInfoSchema: 内存信息模型。
        """
        memory = psutil.virtual_memory()
        return MemoryInfoSchema(
            total=bytes2human(memory.total),
            used=bytes2human(memory.used),
            free=bytes2human(memory.free),
            usage=memory.percent,
        )

    @classmethod
    def _get_system_info(cls) -> SysInfoSchema:
        """
        获取系统信息

        返回:
        - SysInfoSchema: 系统信息模型。
        """
        hostname = socket.gethostname()
        return SysInfoSchema(
            computer_ip=socket.gethostbyname(hostname),
            computer_name=platform.node(),
            os_arch=platform.machine(),
            os_name=platform.platform(),
            user_dir=str(Path.cwd()),
        )

    @classmethod
    def _get_python_info(cls) -> PyInfoSchema:
        """
        获取Python解释器信息

        返回:
        - PyInfoSchema: Python解释器信息模型。
        """
        current_process = psutil.Process()
        memory = psutil.virtual_memory()
        process_memory = current_process.memory_info()

        start_time = current_process.create_time()
        run_time = ServerService._calculate_run_time(start_time)

        return PyInfoSchema(
            name=current_process.name(),
            version=platform.python_version(),
            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
            run_time=run_time,
            home=str(Path(current_process.exe())),
            memory_total=bytes2human(memory.available),
            memory_used=bytes2human(process_memory.rss),
            memory_free=bytes2human(memory.available - process_memory.rss),
            memory_usage=round((process_memory.rss / memory.available) * 100, 2),
        )

    @classmethod
    def _get_disk_info(cls) -> list[DiskInfoSchema]:
        """
        获取磁盘信息

        返回:
        - list[DiskInfoSchema]: 磁盘信息模型列表。
        """
        disk_info = []
        for partition in psutil.disk_partitions():
            try:
                # 使用mountpoint而不是device来获取磁盘使用情况
                usage = psutil.disk_usage(partition.mountpoint)
                mount_point = str(Path(partition.mountpoint))
                disk_info.append(
                    DiskInfoSchema(
                        dir_name=mount_point,  # 使用mountpoint替代device
                        sys_type_name=partition.fstype,
                        type_name=f"本地固定磁盘（{mount_point}）",
                        total=bytes2human(usage.total),
                        used=bytes2human(usage.used),
                        free=bytes2human(usage.free),
                        usage=usage.percent,  # 直接使用数字而不是字符串
                    )
                )
            except (PermissionError, FileNotFoundError):
                # 明确指定可能的异常
                continue
        return disk_info

    @classmethod
    def _calculate_run_time(cls, start_time: float) -> str:
        """
        计算运行时间

        参数:
        - start_time (float): 进程启动时间（时间戳）

        返回:
        - str: 格式化后的运行时间字符串（例如："1天2小时3分钟"）
        """
        difference = time.time() - start_time
        days = int(difference // (24 * 60 * 60))
        hours = int((difference % (24 * 60 * 60)) // (60 * 60))
        minutes = int((difference % (60 * 60)) // 60)
        return f"{days}天{hours}小时{minutes}分钟"
