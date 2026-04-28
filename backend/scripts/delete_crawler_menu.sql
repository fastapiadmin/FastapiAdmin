-- 删除爬虫管理菜单，解决前端路由匹配错误
-- 执行日期: 2026-04-26

USE fastapiadmin;

-- 1. 查看爬虫管理菜单
SELECT id, name, route_name, route_path, type, parent_id
FROM sys_menu
WHERE route_name = 'ConsultationCrawler' OR name LIKE '%爬虫%';

-- 2. 删除爬虫管理菜单的角色关联
DELETE FROM sys_role_menu
WHERE menu_id IN (
    SELECT id FROM sys_menu WHERE route_name = 'ConsultationCrawler'
);

-- 3. 删除爬虫管理菜单的子菜单（按钮权限）
DELETE FROM sys_menu
WHERE parent_id IN (
    SELECT id FROM (
        SELECT id FROM sys_menu WHERE route_name = 'ConsultationCrawler'
    ) AS temp
);

-- 4. 删除爬虫管理菜单
DELETE FROM sys_menu
WHERE route_name = 'ConsultationCrawler';

-- 5. 验证删除结果
SELECT id, name, route_name
FROM sys_menu
WHERE route_name = 'ConsultationCrawler' OR name LIKE '%爬虫%';
