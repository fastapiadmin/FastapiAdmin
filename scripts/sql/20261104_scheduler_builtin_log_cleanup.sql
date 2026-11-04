-- 将默认「日志保留清理」任务迁移到内置同步处理器（MySQL 8+）
-- 背景：旧 func 在线程池里 asyncio.run(...)，异步 DB engine 绑定主事件循环会报 different loop。
-- 幂等：只替换仍是旧代码块的任务。
UPDATE task_cornjob_node
SET func = 'builtin:system_log.cleanup_expired_logs', updated_time = NOW()
WHERE code = 'log_cleanup'
  AND is_deleted = 0
  AND func LIKE 'def handler(%';
