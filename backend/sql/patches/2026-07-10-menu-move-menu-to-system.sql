-- 将「菜单管理」从 平台管理(1) 移动到 系统管理(2) 下,置首位
-- 关联需求: 前端左侧栏把菜单管理归入系统管理
-- 说明: 仅改 parent_id + order；route_path='menu'(相对)会随父级由 /platform/menu 变为 /system/menu；
--       component_path / permission / route_name 与位置无关,不改;6 个按钮子节点(43-48)parent_id=14 随父自动迁移,无需改。

-- ↓↓↓ 正向 ↓↓↓
UPDATE platform_menu SET parent_id = 2, `order` = 0 WHERE id = 14;

-- ↓↓↓ 回滚（恢复到平台管理下,原 order=1）↓↓↓
-- UPDATE platform_menu SET parent_id = 1, `order` = 1 WHERE id = 14;
