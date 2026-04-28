"""
调试菜单数据结构，检查可能导致前端黑屏的问题
"""
import json

# 模拟一个可能导致问题的菜单结构
def check_menu_issues():
    """检查菜单结构问题"""

    issues = []

    # 读取菜单添加脚本中的菜单定义
    menu_definitions = [
        {
            "name": "招生咨询会管理",
            "type": 1,
            "route_path": "/consultation",
            "redirect": "/consultation/info",
            "children": [
                {"name": "咨询会信息", "type": 2, "route_path": "/consultation/info", "component_path": "module_consultation/consultation/index"},
                {"name": "咨询会筛选", "type": 2, "route_path": "/consultation/screening", "component_path": "module_consultation/screening/index"},
                {"name": "报名管理", "type": 2, "route_path": "/consultation/registration", "component_path": "module_consultation/registration/index"},
                {"name": "行程方案", "type": 2, "route_path": "/consultation/itinerary", "component_path": "module_consultation/itinerary/index"},
                {"name": "合规诊断", "type": 2, "route_path": "/consultation/compliance", "component_path": "module_consultation/compliance/index"},
            ]
        }
    ]

    for menu in menu_definitions:
        # 检查1: 目录菜单必须有重定向
        if menu["type"] == 1:
            if not menu.get("redirect"):
                issues.append(f"❌ 目录菜单 '{menu['name']}' 缺少重定向地址")
            else:
                print(f"✅ 目录菜单 '{menu['name']}' 重定向: {menu['redirect']}")

        # 检查2: 子菜单路径是否正确
        if menu.get("children"):
            for child in menu["children"]:
                if child["type"] == 2:
                    if not child.get("component_path"):
                        issues.append(f"❌ 菜单 '{child['name']}' 缺少组件路径")
                    else:
                        print(f"✅ 菜单 '{child['name']}' 组件: {child['component_path']}")

                    # 检查3: 路由路径格式
                    route_path = child.get("route_path", "")
                    if not route_path.startswith("/"):
                        issues.append(f"❌ 菜单 '{child['name']}' 路由路径不以 / 开头: {route_path}")

    # 检查4: 路径冲突
    all_paths = []
    for menu in menu_definitions:
        if menu.get("route_path"):
            all_paths.append((menu["name"], menu["route_path"]))
        if menu.get("children"):
            for child in menu["children"]:
                if child.get("route_path"):
                    all_paths.append((child["name"], child["route_path"]))

    path_set = set()
    for name, path in all_paths:
        if path in path_set:
            issues.append(f"❌ 路由路径冲突: '{name}' 使用路径 '{path}'")
        path_set.add(path)

    print("\n" + "=" * 60)
    if issues:
        print("发现以下问题:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ 菜单结构检查通过，未发现明显问题")
    print("=" * 60)

    print("\n可能的前端黑屏原因:")
    print("1. 组件路径不存在 (module_consultation/xxx/index)")
    print("2. 组件文件有语法错误")
    print("3. 路由循环重定向")
    print("4. 菜单数据递归层级过深")
    print("5. 浏览器控制台报错")

    return issues


if __name__ == "__main__":
    check_menu_issues()
