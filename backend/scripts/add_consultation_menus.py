"""
自动添加招生咨询会管理模块菜单的脚本
"""
import requests
import json

BASE_URL = "http://localhost:18001/api/v1"

def login():
    """登录获取token"""
    login_url = f"{BASE_URL}/system/auth/login"
    data = {
        "username": "admin",
        "password": "123456",
        "login_type": "PC端"
    }
    response = requests.post(login_url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200:
            token = result["data"]["access_token"]
            print(f"✅ 登录成功，token: {token[:20]}...")
            return token
        else:
            print(f"❌ 登录失败: {result}")
            return None
    else:
        print(f"❌ 登录请求失败: {response.status_code} - {response.text}")
        return None

def add_menu(menu_data, headers):
    """添加菜单"""
    url = f"{BASE_URL}/system/menu/create"
    response = requests.post(url, json=menu_data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200:
            menu_id = result["data"]["id"]
            print(f"✅ 菜单 '{menu_data['name']}' 添加成功，ID: {menu_id}")
            return menu_id
        else:
            print(f"❌ 菜单 '{menu_data['name']}' 添加失败: {result}")
            return None
    else:
        print(f"❌ 菜单 '{menu_data['name']}' 请求失败: {response.status_code} - {response.text}")
        return None

def get_parent_menu_id(parent_name, headers):
    """获取父菜单ID"""
    url = f"{BASE_URL}/system/menu/tree"
    params = {"name": parent_name} if parent_name else {}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200 and result["data"]:
            return result["data"][0]["id"]
    return None

def main():
    print("=" * 50)
    print("招生咨询会管理模块 - 自动添加菜单")
    print("=" * 50)

    # 登录
    token = login()
    if not token:
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. 添加一级菜单 - 招生咨询会管理
    print("\n📝 添加一级菜单...")
    parent_menu = {
        "name": "招生咨询会管理",
        "type": 1,
        "order": 10,
        "icon": "document",
        "route_name": "Consultation",
        "route_path": "/consultation",
        "hidden": False,
        "keep_alive": True,
        "always_show": False,
        "title": "招生咨询会管理",
        "parent_id": None,
        "status": "0"
    }
    parent_id = add_menu(parent_menu, headers)
    if not parent_id:
        print("❌ 添加一级菜单失败，退出")
        return

    # 2. 添加二级菜单 - 咨询会信息
    print("\n📝 添加二级菜单...")
    info_menu = {
        "name": "咨询会信息",
        "type": 2,
        "order": 1,
        "permission": "module_consultation:info_collection:query",
        "icon": "table",
        "route_name": "ConsultationInfo",
        "route_path": "/consultation/info",
        "component_path": "module_consultation/consultation/index",
        "hidden": False,
        "keep_alive": True,
        "always_show": False,
        "title": "咨询会信息",
        "parent_id": parent_id,
        "status": "0"
    }
    info_id = add_menu(info_menu, headers)

    # 添加咨询会信息的按钮权限
    print("\n📝 添加咨询会信息按钮权限...")
    info_buttons = [
        ("新增", "module_consultation:info_collection:create"),
        ("编辑", "module_consultation:info_collection:update"),
        ("删除", "module_consultation:info_collection:delete"),
        ("审核", "module_consultation:info_collection:approve"),
        ("归档", "module_consultation:info_collection:archive"),
        ("导出", "module_consultation:info_collection:export"),
        ("导入", "module_consultation:info_collection:import"),
    ]
    for btn_name, btn_perm in info_buttons:
        btn_menu = {
            "name": btn_name,
            "type": 3,
            "order": 1,
            "permission": btn_perm,
            "parent_id": info_id,
            "status": "0"
        }
        add_menu(btn_menu, headers)

    # 3. 添加二级菜单 - 咨询会筛选
    print("\n📝 添加二级菜单...")
    screening_menu = {
        "name": "咨询会筛选",
        "type": 2,
        "order": 2,
        "permission": "module_consultation:screening:query",
        "icon": "filter",
        "route_name": "ConsultationScreening",
        "route_path": "/consultation/screening",
        "component_path": "module_consultation/screening/index",
        "hidden": False,
        "keep_alive": True,
        "always_show": False,
        "title": "咨询会筛选",
        "parent_id": parent_id,
        "status": "0"
    }
    screening_id = add_menu(screening_menu, headers)

    # 添加筛选的按钮权限
    print("\n📝 添加咨询会筛选按钮权限...")
    screening_buttons = [
        ("新增筛选", "module_consultation:screening:create"),
        ("编辑筛选", "module_consultation:screening:update"),
        ("删除筛选", "module_consultation:screening:delete"),
        ("应用筛选", "module_consultation:screening:apply"),
    ]
    for btn_name, btn_perm in screening_buttons:
        btn_menu = {
            "name": btn_name,
            "type": 3,
            "order": 1,
            "permission": btn_perm,
            "parent_id": screening_id,
            "status": "0"
        }
        add_menu(btn_menu, headers)

    # 4. 添加二级菜单 - 报名管理
    print("\n📝 添加二级菜单...")
    registration_menu = {
        "name": "报名管理",
        "type": 2,
        "order": 3,
        "permission": "module_consultation:registration:query",
        "icon": "list",
        "route_name": "ConsultationRegistration",
        "route_path": "/consultation/registration",
        "component_path": "module_consultation/registration/index",
        "hidden": False,
        "keep_alive": True,
        "always_show": False,
        "title": "报名管理",
        "parent_id": parent_id,
        "status": "0"
    }
    registration_id = add_menu(registration_menu, headers)

    # 添加报名的按钮权限
    print("\n📝 添加报名管理按钮权限...")
    registration_buttons = [
        ("新增报名", "module_consultation:registration:create"),
        ("编辑报名", "module_consultation:registration:update"),
        ("删除报名", "module_consultation:registration:delete"),
        ("审核通过", "module_consultation:registration:approve"),
        ("审核拒绝", "module_consultation:registration:reject"),
        ("取消报名", "module_consultation:registration:cancel"),
        ("确认支付", "module_consultation:registration:pay"),
    ]
    for btn_name, btn_perm in registration_buttons:
        btn_menu = {
            "name": btn_name,
            "type": 3,
            "order": 1,
            "permission": btn_perm,
            "parent_id": registration_id,
            "status": "0"
        }
        add_menu(btn_menu, headers)

    # 5. 添加二级菜单 - 行程方案
    print("\n📝 添加二级菜单...")
    itinerary_menu = {
        "name": "行程方案",
        "type": 2,
        "order": 4,
        "permission": "module_consultation:itinerary:query",
        "icon": "route",
        "route_name": "ConsultationItinerary",
        "route_path": "/consultation/itinerary",
        "component_path": "module_consultation/itinerary/index",
        "hidden": False,
        "keep_alive": True,
        "always_show": False,
        "title": "行程方案",
        "parent_id": parent_id,
        "status": "0"
    }
    itinerary_id = add_menu(itinerary_menu, headers)

    # 添加行程的按钮权限
    print("\n📝 添加行程方案按钮权限...")
    itinerary_buttons = [
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
        btn_menu = {
            "name": btn_name,
            "type": 3,
            "order": 1,
            "permission": btn_perm,
            "parent_id": itinerary_id,
            "status": "0"
        }
        add_menu(btn_menu, headers)

    # 6. 添加二级菜单 - 合规诊断
    print("\n📝 添加二级菜单...")
    compliance_menu = {
        "name": "合规诊断",
        "type": 2,
        "order": 5,
        "permission": "module_consultation:compliance:query",
        "icon": "document-checked",
        "route_name": "ConsultationCompliance",
        "route_path": "/consultation/compliance",
        "component_path": "module_consultation/compliance/index",
        "hidden": False,
        "keep_alive": True,
        "always_show": False,
        "title": "合规诊断",
        "parent_id": parent_id,
        "status": "0"
    }
    compliance_id = add_menu(compliance_menu, headers)

    # 添加合规的按钮权限
    print("\n📝 添加合规诊断按钮权限...")
    compliance_buttons = [
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
        btn_menu = {
            "name": btn_name,
            "type": 3,
            "order": 1,
            "permission": btn_perm,
            "parent_id": compliance_id,
            "status": "0"
        }
        add_menu(btn_menu, headers)

    print("\n" + "=" * 50)
    print("✅ 菜单添加完成！")
    print("=" * 50)
    print("\n📋 菜单结构：")
    print("""
招生咨询会管理
├── 咨询会信息
│   ├── 查询
│   ├── 新增
│   ├── 编辑
│   ├── 删除
│   ├── 审核
│   ├── 归档
│   ├── 导出
│   └── 导入
├── 咨询会筛选
│   ├── 新增筛选
│   ├── 编辑筛选
│   ├── 删除筛选
│   └── 应用筛选
├── 报名管理
│   ├── 新增报名
│   ├── 编辑报名
│   ├── 删除报名
│   ├── 审核通过
│   ├── 审核拒绝
│   ├── 取消报名
│   └── 确认支付
├── 行程方案
│   ├── 新增行程
│   ├── 编辑行程
│   ├── 删除行程
│   ├── 确认行程
│   ├── 执行行程
│   ├── 归档行程
│   ├── 同步日历
│   └── 优化路线
└── 合规诊断
    ├── 新增诊断
    ├── 编辑诊断
    ├── 删除诊断
    ├── 执行检查
    ├── 新增规则
    ├── 编辑规则
    ├── 删除规则
    └── 切换状态
""")

if __name__ == "__main__":
    main()
