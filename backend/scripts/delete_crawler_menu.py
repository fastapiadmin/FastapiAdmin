"""
删除爬虫管理菜单，解决前端路由匹配错误
"""
import pymysql


def main():
    # 数据库配置
    DB_CONFIG = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "ServBay.dev",
        "database": "fastapiadmin",
        "charset": "utf8mb4"
    }

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("=" * 60)
        print("删除爬虫管理菜单")
        print("=" * 60)

        # 1. 查找爬虫管理菜单
        cursor.execute(
            "SELECT id, name, route_name FROM sys_menu WHERE route_name = 'ConsultationCrawler'"
        )
        crawler_menu = cursor.fetchone()

        if not crawler_menu:
            print("⚠️ 未找到 ConsultationCrawler 菜单")
            # 尝试查找其他爬虫相关菜单
            cursor.execute(
                "SELECT id, name, route_name FROM sys_menu WHERE name LIKE '%爬虫%'"
            )
            menus = cursor.fetchall()
            if menus:
                print(f"\n找到 {len(menus)} 个爬虫相关菜单:")
                for menu in menus:
                    print(f"  ID={menu[0]}, 名称={menu[1]}, 路由={menu[2]}")
            else:
                print("未找到任何爬虫相关菜单")
            return

        menu_id, name, route_name = crawler_menu
        print(f"\n找到菜单: {name} (ID={menu_id}, 路由={route_name})")

        # 2. 查找子菜单（按钮权限）
        cursor.execute(
            "SELECT id, name FROM sys_menu WHERE parent_id = %s",
            (menu_id,)
        )
        children = cursor.fetchall()
        print(f"找到 {len(children)} 个子菜单/按钮")

        # 3. 删除角色菜单关联
        cursor.execute(
            "DELETE FROM sys_role_menu WHERE menu_id = %s OR menu_id IN (SELECT id FROM (SELECT id FROM sys_menu WHERE parent_id = %s) AS temp)",
            (menu_id, menu_id)
        )
        print(f"✅ 已删除角色菜单关联")

        # 4. 删除子菜单
        cursor.execute(
            "DELETE FROM sys_menu WHERE parent_id = %s",
            (menu_id,)
        )
        print(f"✅ 已删除 {len(children)} 个子菜单")

        # 5. 删除主菜单
        cursor.execute(
            "DELETE FROM sys_menu WHERE id = %s",
            (menu_id,)
        )
        print(f"✅ 已删除主菜单: {name}")

        conn.commit()

        print("\n" + "=" * 60)
        print("✅ 删除完成！")
        print("=" * 60)
        print("\n💡 请刷新页面或重新登录系统")

    except pymysql.err.OperationalError as e:
        print(f"\n❌ 数据库连接失败: {e}")
        print("\n请手动执行 SQL:")
        print("  DELETE FROM sys_menu WHERE route_name = 'ConsultationCrawler';")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    main()
