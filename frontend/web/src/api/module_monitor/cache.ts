import request from '@/utils/http';

const API_PATH = '/monitor/cache';

const CacheAPI = {
  /**
   * 获取缓存信息
   * @returns 缓存信息
   */
  getCacheInfo() {
    return request({
      url: `${API_PATH}/info`,
      method: 'get',
    });
  },

  /**
   * 获取所有缓存名称
   * @returns 所有缓存名称
   */
  getCacheNames() {
    return request({
      url: `${API_PATH}/get/names`,
      method: 'get',
    });
  },

  /**
   * 获取指定缓存名称下的所有键
   * @param cacheName 缓存名称
   * @returns 所有键
   */
  getCacheKeys(cacheName: string) {
    return request({
      url: `${API_PATH}/get/keys/${cacheName}`,
      method: 'get',
    });
  },

  /**
   * 获取指定缓存名称下的指定键的值
   * @param cacheName 缓存名称
   * @param cacheKey 键
   * @returns 值
   */
  getCacheValue(cacheName: string, cacheKey: string) {
    return request({
      url: `${API_PATH}/get/value/${cacheName}/${cacheKey}`,
      method: 'get',
    });
  },

  /**
   * 删除指定缓存名称
   * @param cacheName 缓存名称
   */
  deleteCacheName(cacheName: string) {
    return request({
      url: `${API_PATH}/delete/name/${cacheName}`,
      method: 'delete',
    });
  },

  /**
   * 删除指定缓存名称下的指定键
   * @param cacheName 缓存名称
   * @param cacheKey 键
   */
  deleteCacheKey(cacheKey: string) {
    return request({
      url: `${API_PATH}/delete/key/${cacheKey}`,
      method: 'delete',
    });
  },

  /**
   * 删除所有缓存
   */
  deleteCacheAll() {
    return request({
      url: `${API_PATH}/delete/all`,
      method: 'delete',
    });
  },
};

export default CacheAPI;

export interface CacheForm {
  cache_name: string;
  cache_key: string;
  cache_value: string;
}

export interface CacheInfo {
  cache_key: string;
  cache_name: string;
  cache_value: string;
  remark: string;
}

export interface CommandStats {
  name: string;
  value: string;
}

export interface RedisInfo {
  redis_version: string;
  redis_mode: string;
  tcp_port: number;
  connected_clients: number;
  uptime_in_days: number;
  used_memory_human: string;
  used_cpu_user_children: string;
  maxmemory_human: string;
  aof_enabled: string;
  rdb_last_bgsave_status: string;
  instantaneous_input_kbps: number;
  instantaneous_output_kbps: number;
}

export interface CacheMonitor {
  command_stats: CommandStats[];
  db_size: number;
  info: RedisInfo;
}
