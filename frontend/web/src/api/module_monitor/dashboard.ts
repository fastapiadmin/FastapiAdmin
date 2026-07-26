import { request } from "@utils";

const API_PATH = "/monitor/online";

export interface RecentLoginItem {
  username: string;
  status: number; // 1:成功 2:失败
  login_time: string;
  login_ip?: string;
  login_location?: string;
}

export interface DashboardStats {
  online_users: number;
  total_users: number;
  today_login_count: number;
  today_unique_users: number;
  week_user_created: number;
  recent_logins: RecentLoginItem[];
}

const DashboardAPI = {
  getStats() {
    return request<ApiResponse<DashboardStats>>({
      url: `${API_PATH}/stats`,
      method: "get",
    });
  },
};

export default DashboardAPI;
