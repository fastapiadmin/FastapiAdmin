"""
直接通过数据库添加招生宣传活动模块菜单
"""
import pymysql
import uuid
import os
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
    print("招生宣传活动模块 - 直接添加菜单到数据库")
    print("=" * 50)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. 添加一级菜单 - 招生宣传活动
        print("\n📝 添加一级菜单...")
        parent_menu_id = insert_menu(
            cursor=cursor,
            name="招生宣传活动",
            menu_type=1,
            order=11,
            permission=None,
            icon="Menu",
            route_name="Promotion",
            route_path="/promotion",
            component_path=None,
            hidden=False,
            keep_alive=False,
            always_show=True,
            title="招生宣传活动",
            parent_id=None,
            status="0",
            description="招生宣传活动管理模块"
        )
        print(f"✅ 招生宣传活动 添加成功，ID: {parent_menu_id}")

        # 2. 添加二级菜单 - 组织架构管理
        print("\n📝 添加二级菜单...")
        team_id = insert_menu(
            cursor=cursor,
            name="组织架构管理",
            menu_type=2,
            order=1,
            permission="module_promotion:team:query",
            icon="el-icon-s-custom",
            route_name="PromotionTeam",
            route_path="/promotion/team",
            component_path="module_promotion/team/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="组织架构管理",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 组织架构管理 添加成功，ID: {team_id}")

        # 添加组织架构管理的按钮权限
        print("\n📝 添加组织架构管理按钮权限...")
        team_buttons = [
            ("查询", "module_promotion:team:query"),
            ("新增", "module_promotion:team:create"),
            ("编辑", "module_promotion:team:update"),
            ("删除", "module_promotion:team:delete"),
        ]
        for btn_name, btn_perm in team_buttons:
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
                parent_id=team_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 3. 添加二级菜单 - 人员管理
        print("\n📝 添加二级菜单...")
        personnel_id = insert_menu(
            cursor=cursor,
            name="人员管理",
            menu_type=2,
            order=2,
            permission="module_promotion:personnel:query",
            icon="User",
            route_name="PromotionPersonnel",
            route_path="/promotion/personnel",
            component_path="module_promotion/personnel/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="人员管理",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 人员管理 添加成功，ID: {personnel_id}")

        personnel_buttons = [
            ("查询", "module_promotion:personnel:query"),
            ("新增", "module_promotion:personnel:create"),
            ("编辑", "module_promotion:personnel:update"),
            ("删除", "module_promotion:personnel:delete"),
            ("邀请", "module_promotion:personnel:invite"),
        ]
        for btn_name, btn_perm in personnel_buttons:
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
                parent_id=personnel_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 4. 添加二级菜单 - 目标学校管理
        print("\n📝 添加二级菜单...")
        target_school_id = insert_menu(
            cursor=cursor,
            name="目标学校管理",
            menu_type=2,
            order=3,
            permission="module_promotion:target_school:query",
            icon="School",
            route_name="PromotionTargetSchool",
            route_path="/promotion/target-school",
            component_path="module_promotion/target_school/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="目标学校管理",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 目标学校管理 添加成功，ID: {target_school_id}")

        target_school_buttons = [
            ("查询", "module_promotion:target_school:query"),
            ("新增", "module_promotion:target_school:create"),
            ("编辑", "module_promotion:target_school:update"),
            ("删除", "module_promotion:target_school:delete"),
            ("跟进", "module_promotion:target_school:follow"),
        ]
        for btn_name, btn_perm in target_school_buttons:
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
                parent_id=target_school_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 5. 添加二级菜单 - 活动申请审批
        print("\n📝 添加二级菜单...")
        activity_apply_id = insert_menu(
            cursor=cursor,
            name="活动申请审批",
            menu_type=2,
            order=4,
            permission="module_promotion:activity_apply:query",
            icon="Calendar",
            route_name="PromotionActivityApply",
            route_path="/promotion/activity-apply",
            component_path="module_promotion/activity_apply/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="活动申请审批",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 活动申请审批 添加成功，ID: {activity_apply_id}")

        activity_apply_buttons = [
            ("查询", "module_promotion:activity_apply:query"),
            ("新增申请", "module_promotion:activity_apply:create"),
            ("编辑", "module_promotion:activity_apply:update"),
            ("删除", "module_promotion:activity_apply:delete"),
            ("审批", "module_promotion:activity_apply:approve"),
        ]
        for btn_name, btn_perm in activity_apply_buttons:
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
                parent_id=activity_apply_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 6. 添加二级菜单 - 物料管理
        print("\n📝 添加二级菜单...")
        material_id = insert_menu(
            cursor=cursor,
            name="物料管理",
            menu_type=2,
            order=5,
            permission="module_promotion:material:query",
            icon="Box",
            route_name="PromotionMaterial",
            route_path="/promotion/material",
            component_path="module_promotion/material/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="物料管理",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 物料管理 添加成功，ID: {material_id}")

        material_buttons = [
            ("查询", "module_promotion:material:query"),
            ("新增", "module_promotion:material:create"),
            ("编辑", "module_promotion:material:update"),
            ("删除", "module_promotion:material:delete"),
            ("申领", "module_promotion:material:apply"),
            ("发放", "module_promotion:material:issue"),
        ]
        for btn_name, btn_perm in material_buttons:
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
                parent_id=material_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 7. 添加二级菜单 - 行程报备
        print("\n📝 添加二级菜单...")
        trip_id = insert_menu(
            cursor=cursor,
            name="行程报备",
            menu_type=2,
            order=6,
            permission="module_promotion:trip:query",
            icon="Location",
            route_name="PromotionTrip",
            route_path="/promotion/trip",
            component_path="module_promotion/trip/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="行程报备",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 行程报备 添加成功，ID: {trip_id}")

        trip_buttons = [
            ("查询", "module_promotion:trip:query"),
            ("报备", "module_promotion:trip:create"),
            ("编辑", "module_promotion:trip:update"),
            ("删除", "module_promotion:trip:delete"),
            ("位置共享", "module_promotion:trip:location"),
        ]
        for btn_name, btn_perm in trip_buttons:
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
                parent_id=trip_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 8. 添加二级菜单 - 费用报销
        print("\n📝 添加二级菜单...")
        expense_id = insert_menu(
            cursor=cursor,
            name="费用报销",
            menu_type=2,
            order=7,
            permission="module_promotion:expense:query",
            icon="Money",
            route_name="PromotionExpense",
            route_path="/promotion/expense",
            component_path="module_promotion/expense/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="费用报销",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 费用报销 添加成功，ID: {expense_id}")

        expense_buttons = [
            ("查询", "module_promotion:expense:query"),
            ("申请", "module_promotion:expense:create"),
            ("编辑", "module_promotion:expense:update"),
            ("删除", "module_promotion:expense:delete"),
            ("审批", "module_promotion:expense:approve"),
            ("报销", "module_promotion:expense:reimburse"),
        ]
        for btn_name, btn_perm in expense_buttons:
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
                parent_id=expense_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 9. 添加二级菜单 - 活动打卡
        print("\n📝 添加二级菜单...")
        checkin_id = insert_menu(
            cursor=cursor,
            name="活动打卡",
            menu_type=2,
            order=8,
            permission="module_promotion:checkin:query",
            icon="Clock",
            route_name="PromotionCheckin",
            route_path="/promotion/checkin",
            component_path="module_promotion/checkin/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="活动打卡",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 活动打卡 添加成功，ID: {checkin_id}")

        checkin_buttons = [
            ("查询", "module_promotion:checkin:query"),
            ("打卡", "module_promotion:checkin:do"),
            ("编辑", "module_promotion:checkin:update"),
            ("删除", "module_promotion:checkin:delete"),
        ]
        for btn_name, btn_perm in checkin_buttons:
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
                parent_id=checkin_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 10. 添加二级菜单 - 总结上传
        print("\n📝 添加二级菜单...")
        summary_id = insert_menu(
            cursor=cursor,
            name="总结上传",
            menu_type=2,
            order=9,
            permission="module_promotion:summary:query",
            icon="Document",
            route_name="PromotionSummary",
            route_path="/promotion/summary",
            component_path="module_promotion/summary/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="总结上传",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 总结上传 添加成功，ID: {summary_id}")

        summary_buttons = [
            ("查询", "module_promotion:summary:query"),
            ("上传", "module_promotion:summary:create"),
            ("编辑", "module_promotion:summary:update"),
            ("删除", "module_promotion:summary:delete"),
            ("归档", "module_promotion:summary:archive"),
        ]
        for btn_name, btn_perm in summary_buttons:
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
                parent_id=summary_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 11. 添加二级菜单 - 活动撰写
        print("\n📝 添加二级菜单...")
        document_id = insert_menu(
            cursor=cursor,
            name="活动撰写",
            menu_type=2,
            order=10,
            permission="module_promotion:document:query",
            icon="Edit",
            route_name="PromotionDocument",
            route_path="/promotion/document",
            component_path="module_promotion/document/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="活动撰写",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 活动撰写 添加成功，ID: {document_id}")

        document_buttons = [
            ("查询", "module_promotion:document:query"),
            ("生成", "module_promotion:document:create"),
            ("编辑", "module_promotion:document:update"),
            ("删除", "module_promotion:document:delete"),
            ("推送", "module_promotion:document:push"),
        ]
        for btn_name, btn_perm in document_buttons:
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
                parent_id=document_id,
                status="0"
            )
            print(f"  ✅ {btn_name} 添加成功，ID: {btn_id}")

        # 12. 添加二级菜单 - 表彰评优
        print("\n📝 添加二级菜单...")
        evaluation_id = insert_menu(
            cursor=cursor,
            name="表彰评优",
            menu_type=2,
            order=11,
            permission="module_promotion:evaluation:query",
            icon="Trophy",
            route_name="PromotionEvaluation",
            route_path="/promotion/evaluation",
            component_path="module_promotion/evaluation/index",
            hidden=False,
            keep_alive=True,
            always_show=False,
            title="表彰评优",
            parent_id=parent_menu_id,
            status="0"
        )
        print(f"✅ 表彰评优 添加成功，ID: {evaluation_id}")

        evaluation_buttons = [
            ("查询", "module_promotion:evaluation:query"),
            ("发起", "module_promotion:evaluation:create"),
            ("编辑", "module_promotion:evaluation:update"),
            ("删除", "module_promotion:evaluation:delete"),
            ("成果统计", "module_promotion:evaluation:stat"),
        ]
        for btn_name, btn_perm in evaluation_buttons:
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
                parent_id=evaluation_id,
                status="0"
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
