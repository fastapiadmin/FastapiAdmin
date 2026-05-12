"""
直接通过数据库添加招生咨询会管理模块菜单
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
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('DATABASE_PASSWORD'):
                _, value = line.split('=', 1)
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
        "charset": "utf8mb4"
    }

DB_CONFIG = load_db_config()

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)

def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4()).replace("-", "")

def insert_menu(cursor, name, menu_type, order, permission, icon, route_name, route_path,
                component_path, hidden, keep_alive, always_show, title, parent_id, status,
                description=None, redirect=None):
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
        menu_uuid, name, menu_type, order, permission, icon, route_name, route_path,
        component_path, redirect, hidden, keep_alive, always_show, title,
        parent_id, status, description, False, now, now
    )

    cursor.execute(sql, values)
    menu_id = cursor.lastrowid
    return menu_id

def main():
    print("=" * 50)
    print("招生咨询会管理模块 - 直接添加菜单到数据库")
    print("=" * 50)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. 添加一级菜单 - 招生咨询会管理
        print("\n📝 添加一级菜单...")
        parent_menu_id = insert_menu(
            cursor=cursor,
            name="招生咨询会管理",
            menu_type=1,
            order=10,
            permission=None,
            icon="document",
            route_name="Consultation",
            route_path="/consultation",
            component_path=None,
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="招生咨询会管理",
            parent_id=None,
            status="0",
            description="招生咨询会管理模块"
        )
        print(f"✅ 招生咨询会管理 添加成功，ID: {parent_menu_id}")

        # 2. 添加二级菜单 - 咨询会信息
        print("\n📝 添加二级菜单...")
        info_id = insert_menu(
            cursor=cursor,
            name="咨询会信息",
            menu_type=2,
            order=1,
            permission="module_consultation:info_collection:query",
            icon="table",
            route_name="ConsultationInfo",
            route_path="/consultation/info",
            component_path="module_consultation/consultation/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="咨询会信息",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 咨询会信息 添加成功，ID: {info_id}")

        # 添加咨询会信息的按钮权限
        print("\n📝 添加咨询会信息按钮权限...")
        info_buttons = [
            ("查询", "module_consultation:info_collection:query"),
            ("新增", "module_consultation:info_collection:create"),
            ("编辑", "module_consultation:info_collection:update"),
            ("删除", "module_consultation:info_collection:delete"),
            ("审核", "module_consultation:info_collection:approve"),
            ("归档", "module_consultation:info_collection:archive"),
            ("导出", "module_consultation:info_collection:export"),
            ("导入", "module_consultation:info_collection:import"),
        ]
        for btn_name, btn_perm in info_buttons:
            btn_id = insert_menu(
                cursor=cursor,
                name=btn_name,
                menu_type=3,
                order=1,
                permission=btn_perm,
                icon=None,
                route_name=None,
                route_path=None,
                component_path=None,
                hidden=False,
                keep_alive=True,
                always_show=False,
                title=btn_name,
                parent_id=info_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 3. 添加二级菜单 - 咨询会筛选
        print("\n📝 添加二级菜单...")
        screening_id = insert_menu(
            cursor=cursor,
            name="咨询会筛选",
            menu_type=2,
            order=2,
            permission="module_consultation:screening:query",
            icon="filter",
            route_name="ConsultationScreening",
            route_path="/consultation/screening",
            component_path="module_consultation/screening/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="咨询会筛选",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 咨询会筛选 添加成功，ID: {screening_id}")

        screening_buttons = [
            ("查询筛选", "module_consultation:screening:query"),
            ("新增筛选", "module_consultation:screening:create"),
            ("编辑筛选", "module_consultation:screening:update"),
            ("删除筛选", "module_consultation:screening:delete"),
            ("应用筛选", "module_consultation:screening:apply"),
        ]
        for btn_name, btn_perm in screening_buttons:
            btn_id = insert_menu(
                cursor=cursor,
                name=btn_name,
                menu_type=3,
                order=1,
                permission=btn_perm,
                icon=None,
                route_name=None,
                route_path=None,
                component_path=None,
                hidden=False,
                keep_alive=True,
                always_show=False,
                title=btn_name,
                parent_id=screening_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 4. 添加二级菜单 - 报名管理
        print("\n📝 添加二级菜单...")
        registration_id = insert_menu(
            cursor=cursor,
            name="报名管理",
            menu_type=2,
            order=3,
            permission="module_consultation:registration:query",
            icon="list",
            route_name="ConsultationRegistration",
            route_path="/consultation/registration",
            component_path="module_consultation/registration/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="报名管理",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 报名管理 添加成功，ID: {registration_id}")

        registration_buttons = [
            ("查询报名", "module_consultation:registration:query"),
            ("新增报名", "module_consultation:registration:create"),
            ("编辑报名", "module_consultation:registration:update"),
            ("删除报名", "module_consultation:registration:delete"),
            ("审核通过", "module_consultation:registration:approve"),
            ("审核拒绝", "module_consultation:registration:reject"),
            ("取消报名", "module_consultation:registration:cancel"),
            ("确认支付", "module_consultation:registration:pay"),
        ]
        for btn_name, btn_perm in registration_buttons:
            btn_id = insert_menu(
                cursor=cursor,
                name=btn_name,
                menu_type=3,
                order=1,
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
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 5. 添加二级菜单 - 行程方案
        print("\n📝 添加二级菜单...")
        itinerary_id = insert_menu(
            cursor=cursor,
            name="行程方案",
            menu_type=2,
            order=4,
            permission="module_consultation:itinerary:query",
            icon="route",
            route_name="ConsultationItinerary",
            route_path="/consultation/itinerary",
            component_path="module_consultation/itinerary/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="行程方案",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 行程方案 添加成功，ID: {itinerary_id}")

        itinerary_buttons = [
            ("查询行程", "module_consultation:itinerary:query"),
            ("新增行程", "module_consultation:itinerary:create"),
            ("编辑行程", "module_consultation:itinerary:update"),
            ("删除行程", "module_consultation:itinerary:delete"),
            ("确认行程", "module_consultation:itinerary:confirm"),
            ("执行行程", "module_consultation:itinerary:execute"),
            ("归档行程", "module_consultation:itinerary:archive"),
            ("同步日历", "module_consultation:itinerary:sync"),
            ("优化路线", "module_consultation:itinerary:optimize"),
        ]
        for btn_name, btn_perm in itinerary_buttons:
            btn_id = insert_menu(
                cursor=cursor,
                name=btn_name,
                menu_type=3,
                order=1,
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
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 6. 添加二级菜单 - 合规诊断
        print("\n📝 添加二级菜单...")
        compliance_id = insert_menu(
            cursor=cursor,
            name="合规诊断",
            menu_type=2,
            order=5,
            permission="module_consultation:compliance:query",
            icon="document-checked",
            route_name="ConsultationCompliance",
            route_path="/consultation/compliance",
            component_path="module_consultation/compliance/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="合规诊断",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 合规诊断 添加成功，ID: {compliance_id}")

        compliance_buttons = [
            ("查询诊断", "module_consultation:compliance:query"),
            ("新增诊断", "module_consultation:compliance:create"),
            ("编辑诊断", "module_consultation:compliance:update"),
            ("删除诊断", "module_consultation:compliance:delete"),
            ("执行检查", "module_consultation:compliance:check"),
            ("新增规则", "module_consultation:compliance:rule:create"),
            ("编辑规则", "module_consultation:compliance:rule:update"),
            ("删除规则", "module_consultation:compliance:rule:delete"),
            ("切换状态", "module_consultation:compliance:rule:toggle"),
        ]
        for btn_name, btn_perm in compliance_buttons:
            btn_id = insert_menu(
                cursor=cursor,
                name=btn_name,
                menu_type=3,
                order=1,
                permission=btn_perm,
                icon=None,
                route_name=None,
                route_path=None,
                component_path=None,
                hidden=False,
                keep_alive=True,
                always_show=False,
                title=btn_name,
                parent_id=compliance_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 7. 添加二级菜单 - 高校信息
        print("\n📝 添加二级菜单...")
        university_id = insert_menu(
            cursor=cursor,
            name="高校信息",
            menu_type=2,
            order=6,
            permission="module_consultation:university:query",
            icon="office-building",
            route_name="ConsultationUniversity",
            route_path="/consultation/university",
            component_path="module_consultation/university/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="高校信息",
            parent_id=parent_menu_id,
            status="0",
            description="咨询会参与高校维护",
        )
        print(f"✅ 高校信息 添加成功，ID: {university_id}")

        university_buttons = [
            ("查询", "module_consultation:university:query"),
            ("详情", "module_consultation:university:detail"),
            ("新增", "module_consultation:university:create"),
            ("编辑", "module_consultation:university:update"),
            ("删除", "module_consultation:university:delete"),
        ]
        for btn_name, btn_perm in university_buttons:
            btn_id = insert_menu(
                cursor=cursor,
                name=btn_name,
                menu_type=3,
                order=1,
                permission=btn_perm,
                icon=None,
                route_name=None,
                route_path=None,
                component_path=None,
                hidden=False,
                keep_alive=True,
                always_show=False,
                title=btn_name,
                parent_id=university_id,
                status="0",
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 提交事务
        conn.commit()
        print("\n" + "=" * 50)
        print("✅ 菜单添加完成！")
        print("=" * 50)

    except Exception as e:
        conn.rollback()
        print(f"\n❌ 发生错误，已回滚: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
