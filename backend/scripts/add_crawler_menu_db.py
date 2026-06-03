"""
幂等添加「全网抓取」菜单（仅超级管理员通过全量菜单可见，不绑定普通角色）
"""
import uuid
from datetime import datetime
from pathlib import Path

import pymysql

CRAWL_PERMISSION = "module_consultation:info_collection:crawl"
CRAWL_ROUTE_PATH = "/consultation/crawler"


def load_db_config():
    env_path = Path(__file__).parent.parent / "env" / ".env.dev"
    if not env_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {env_path}")

    db_password = None
    with open(env_path, encoding="utf-8") as f:
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


def insert_menu(cursor, name, menu_type, order, permission, icon, route_name, route_path,
                component_path, hidden, keep_alive, always_show, title, parent_id, status,
                description=None, redirect=None):
    now = datetime.now()
    menu_uuid = str(uuid.uuid4()).replace("-", "")
    sql = """
    INSERT INTO sys_menu (uuid, name, type, `order`, permission, icon, route_name, route_path,
                          component_path, redirect, hidden, keep_alive, always_show, title,
                          parent_id, status, description, affix, created_time, updated_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        menu_uuid, name, menu_type, order, permission, icon, route_name, route_path,
        component_path, redirect, hidden, keep_alive, always_show, title,
        parent_id, status, description, False, now, now,
    )
    cursor.execute(sql, values)
    return cursor.lastrowid


def main():
    print("=" * 50)
    print("添加「全网抓取」菜单（幂等）")
    print("=" * 50)

    conn = pymysql.connect(**load_db_config())
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM sys_menu WHERE route_path = %s OR permission = %s LIMIT 1",
            (CRAWL_ROUTE_PATH, CRAWL_PERMISSION),
        )
        if cursor.fetchone():
            print("✅ 全网抓取菜单已存在，跳过")
            return

        cursor.execute(
            "SELECT id FROM sys_menu WHERE route_path = %s AND parent_id IS NULL LIMIT 1",
            ("/consultation",),
        )
        row = cursor.fetchone()
        if not row:
            print("❌ 未找到「招生咨询会管理」一级菜单，请先执行 add_consultation_menus_db.py")
            return
        parent_menu_id = row[0]

        crawler_id = insert_menu(
            cursor=cursor,
            name="全网抓取",
            menu_type=2,
            order=2,
            permission=CRAWL_PERMISSION,
            icon="download",
            route_name="ConsultationCrawler",
            route_path=CRAWL_ROUTE_PATH,
            component_path="module_consultation/crawler/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="全网抓取",
            parent_id=parent_menu_id,
            status="0",
            description="超级管理员：手动触发全网抓取",
        )
        print(f"✅ 全网抓取菜单添加成功，ID: {crawler_id}")

        btn_id = insert_menu(
            cursor=cursor,
            name="触发抓取",
            menu_type=3,
            order=1,
            permission=CRAWL_PERMISSION,
            icon=None,
            route_name=None,
            route_path=None,
            component_path=None,
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="触发抓取",
            parent_id=crawler_id,
            status="0",
        )
        print(f"  ✅ 触发抓取按钮权限添加成功，ID: {btn_id}")

        conn.commit()
        print("\n🎉 完成（未分配给普通角色，仅超级管理员可见全部菜单）")
    except Exception as e:
        conn.rollback()
        print(f"❌ 失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
