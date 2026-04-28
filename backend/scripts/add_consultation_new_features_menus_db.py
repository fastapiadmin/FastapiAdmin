"""
直接通过数据库添加招生咨询会管理新功能菜单
新增：一键报名、转发至招生组、看板视图、日历视图、移动任务、预览列表
"""
import pymysql
import uuid
from datetime import datetime
from pathlib import Path


def load_db_config():
    """从 .env.dev 加载数据库配置"""
    env_path = Path(__file__).parent.parent / "env" / ".env.dev"

    if not env_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {env_path}")

    db_password = None
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DATABASE_PASSWORD"):
                _, value = line.split("=", 1)
                db_password = value.strip().strip('"').strip("'")
                break

    if db_password is None:
        raise ValueError("在 .env.dev 中找不到 DATABASE_PASSWORD")

    return {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": db_password,
        "database": "high_school_college",
        "charset": "utf8mb4",
    }


DB_CONFIG = load_db_config()


def get_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4()).replace("-", "")


def insert_menu(
    cursor,
    name,
    menu_type,
    order,
    permission,
    icon,
    route_name,
    route_path,
    component_path,
    hidden,
    keep_alive,
    always_show,
    title,
    parent_id,
    status,
    description=None,
    redirect=None,
):
    """插入菜单"""
    now = datetime.now()
    menu_uuid = generate_uuid()

    sql = """
    INSERT INTO sys_menu (uuid, name, type, `order`, permission, icon, route_name, route_path,
                          component_path, redirect, hidden, keep_alive, always_show, title,
                          parent_id, status, description, affix, created_time, updated_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        menu_uuid,
        name,
        menu_type,
        order,
        permission,
        icon,
        route_name,
        route_path,
        component_path,
        redirect,
        hidden,
        keep_alive,
        always_show,
        title,
        parent_id,
        status,
        description,
        False,
        now,
        now,
    )

    cursor.execute(sql, values)
    menu_id = cursor.lastrowid
    return menu_id


def find_parent_menu_id(cursor, name):
    """根据菜单名称查找父菜单ID"""
    sql = "SELECT id FROM sys_menu WHERE name = %s AND type = 1 LIMIT 1"
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    return result[0] if result else None


def find_sub_menu_id(cursor, name, parent_id):
    """根据菜单名称和父ID查找子菜单ID"""
    sql = "SELECT id FROM sys_menu WHERE name = %s AND parent_id = %s LIMIT 1"
    cursor.execute(sql, (name, parent_id))
    result = cursor.fetchone()
    return result[0] if result else None


def check_permission_exists(cursor, permission):
    """检查权限是否已存在"""
    sql = "SELECT id FROM sys_menu WHERE permission = %s LIMIT 1"
    cursor.execute(sql, (permission,))
    return cursor.fetchone() is not None


def main():
    print("=" * 50)
    print("招生咨询会管理模块 - 添加新功能菜单和权限")
    print("=" * 50)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 查找父菜单 - 招生咨询会管理
        parent_menu_id = find_parent_menu_id(cursor, "招生咨询会管理")
        if not parent_menu_id:
            print("❌ 未找到父菜单 '招生咨询会管理'，请先运行 add_consultation_menus_db.py")
            return
        print(f"✅ 找到父菜单 '招生咨询会管理'，ID: {parent_menu_id}")

        # 查找各子菜单
        info_id = find_sub_menu_id(cursor, "咨询会信息", parent_menu_id)
        registration_id = find_sub_menu_id(cursor, "报名管理", parent_menu_id)
        itinerary_id = find_sub_menu_id(cursor, "行程方案", parent_menu_id)

        print(f"  - 咨询会信息 ID: {info_id}")
        print(f"  - 报名管理 ID: {registration_id}")
        print(f"  - 行程方案 ID: {itinerary_id}")

        # ============================================ #
        # 1. 咨询会信息 - 添加预览列表按钮
        # ============================================ #
        print("\n📝 添加 '咨询会信息' 新增按钮权限...")

        if not check_permission_exists(cursor, "module_consultation:info_collection:preview"):
            preview_id = insert_menu(
                cursor=cursor,
                name="预览列表",
                menu_type=3,
                order=10,
                permission="module_consultation:info_collection:preview",
                icon=None,
                route_name=None,
                route_path=None,
                component_path=None,
                hidden=False,
                keep_alive=True,
                always_show=False,
                title="预览列表",
                parent_id=info_id,
                status="0",
            )
            print(f"  ✅ 预览列表 添加成功，ID: {preview_id}")
        else:
            print("  ⚠️ 预览列表 权限已存在，跳过")

        # ============================================ #
        # 2. 报名管理 - 添加一键报名、转发至招生组按钮
        # ============================================ #
        print("\n📝 添加 '报名管理' 新增按钮权限...")

        new_registration_buttons = [
            ("一键报名", "module_consultation:registration:one_click_register"),
            ("转发至招生组", "module_consultation:registration:forward_to_team"),
        ]

        for btn_name, btn_perm in new_registration_buttons:
            if not check_permission_exists(cursor, btn_perm):
                btn_id = insert_menu(
                    cursor=cursor,
                    name=btn_name,
                    menu_type=3,
                    order=20,
                    permission=btn_perm,
                    icon=None,
                    route_name=None,
                    route_path=None,
                    component_path=None,
                    hidden=False,
                    keep_alive=True,
                    always_show=False,
                    title=btn_name,
                    parent_id=registration_id,
                    status="0",
                )
                print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")
            else:
                print(f"  ⚠️ {btn_name} 权限已存在，跳过")

        # ============================================ #
        # 3. 行程方案 - 添加看板视图、日历视图、移动任务按钮
        # ============================================ #
        print("\n📝 添加 '行程方案' 新增按钮权限...")

        new_itinerary_buttons = [
            ("看板视图", "module_consultation:itinerary:kanban_board"),
            ("日历视图", "module_consultation:itinerary:calendar_board"),
            ("移动任务", "module_consultation:itinerary:move_task"),
        ]

        for btn_name, btn_perm in new_itinerary_buttons:
            if not check_permission_exists(cursor, btn_perm):
                btn_id = insert_menu(
                    cursor=cursor,
                    name=btn_name,
                    menu_type=3,
                    order=20,
                    permission=btn_perm,
                    icon=None,
                    route_name=None,
                    route_path=None,
                    component_path=None,
                    hidden=False,
                    keep_alive=True,
                    always_show=False,
                    title=btn_name,
                    parent_id=itinerary_id,
                    status="0",
                )
                print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")
            else:
                print(f"  ⚠️ {btn_name} 权限已存在，跳过")

        # 提交事务
        conn.commit()
        print("\n" + "=" * 50)
        print("✅ 新功能菜单和权限添加完成！")
        print("=" * 50)
        print("\n新增权限列表：")
        print("  - module_consultation:info_collection:preview (预览列表)")
        print("  - module_consultation:registration:one_click_register (一键报名)")
        print("  - module_consultation:registration:forward_to_team (转发至招生组)")
        print("  - module_consultation:itinerary:kanban_board (看板视图)")
        print("  - module_consultation:itinerary:calendar_board (日历视图)")
        print("  - module_consultation:itinerary:move_task (移动任务)")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ 发生错误，已回滚: {e}")
        import traceback

        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
