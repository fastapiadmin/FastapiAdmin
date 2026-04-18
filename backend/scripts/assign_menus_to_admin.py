"""
分配菜单给admin角色的脚本
"""
import pymysql

def main():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='high_school_college',
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    # 查看管理员角色
    cursor.execute("SELECT id, name FROM sys_role WHERE name='管理员角色'")
    role = cursor.fetchone()
    if role:
        print(f'Admin角色ID: {role[0]}')
        admin_role_id = role[0]

        # 查看新添加的菜单ID (从189开始)
        cursor.execute('SELECT id FROM sys_menu WHERE id >= 189 ORDER BY id')
        menu_ids = [row[0] for row in cursor.fetchall()]
        print(f'新菜单ID数量: {len(menu_ids)}')

        # 分配菜单给admin
        for menu_id in menu_ids:
            try:
                cursor.execute(
                    'INSERT INTO sys_role_menus (role_id, menu_id) VALUES (%s, %s)',
                    (admin_role_id, menu_id)
                )
            except:
                pass  # 忽略已存在的

        conn.commit()
        print('✅ 菜单已分配给admin角色')
    else:
        print('未找到admin角色')

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
