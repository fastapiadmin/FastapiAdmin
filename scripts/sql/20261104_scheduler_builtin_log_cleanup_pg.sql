-- 将默认「日志保留清理」任务迁移到内置同步处理器（PostgreSQL）
UPDATE task_cornjob_node
SET func = 'builtin:system_log.cleanup_expired_logs', updated_time = NOW()
WHERE code = 'log_cleanup'
  AND is_deleted = false
  AND func LIKE 'def handler(%';
