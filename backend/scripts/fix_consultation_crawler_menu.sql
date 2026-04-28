-- 修复 ConsultationCrawler 菜单问题
-- 删除不存在对应页面的爬虫管理菜单

USE fastapiadmin;

-- 查看爬虫管理菜单
SELECT id, name, route_name, route_path, component_path, type, parent_id
FROM sys_menu
WHERE name LIKE '%爬虫%' OR route_name = 'ConsultationCrawler';

-- 删除爬虫管理菜单（如果不存在对应页面）
-- 先删除子菜单（按钮权限）
DELETE FROM sys_menu
WHERE parent_id IN (
    SELECT id FROM (
        SELECT id FROM sys_menu WHERE route_name = 'ConsultationCrawler'
    ) AS temp
);

-- 再删除爬虫管理菜单本身
DELETE FROM sys_menu
WHERE route_name = 'ConsultationCrawler';

-- 同时删除相关的角色菜单关联
DELETE FROM sys_role_menu
WHERE menu_id NOT IN (SELECT id FROM sys_menu);

-- 验证删除结果
SELECT id, name, route_name, route_path
FROM sys_menu
WHERE name LIKE '%爬虫%' OR route_name = 'ConsultationCrawler';
