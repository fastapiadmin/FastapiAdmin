import request from "@/utils/request";

const API_PATH = "/monitor/server";

const ServerAPI = {
  // 获取服务信息
  getServer() {
    return request<ApiResponse>({
      url: `${API_PATH}/info`,
      method: "get",
    });
  },
};

export default ServerAPI;

export interface Cpu {
  cpu_num: number;
  used: number;
  sys: number;
  free: number;
}

export interface Memory {
  total: string;
  used: string;
  free: string;
  usage: number;
}

export interface System {
  computer_name: string;
  os_name: string;
  computer_ip: string;
  os_arch: string;
  user_dir: string;
}

export interface Python {
  name: string;
  version: string;
  start_time: string;
  run_time: string;
  home: string;
  memory_total: string;
  memory_used: string;
  memory_free: string;
  memory_usage: number;
}

export interface SysFile {
  dirName: string;
  sysTypeName: string;
  typeName: string;
  total: string;
  free: string;
  used: string;
  usage: number;
}

export interface ServerInfo {
  cpu: Cpu;
  mem: Memory;
  sys: System;
  py: Python;
  disks: SysFile[];
}
