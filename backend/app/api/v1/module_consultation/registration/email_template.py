"""
报名回执模板服务

提供咨询会报名回执邮件的固定回复版式模板
"""

from typing import Any


class RegistrationEmailTemplate:
    """
    报名回执模板管理

    支持固定回复版式模板的获取和自定义
    """

    # 默认模板（可编辑）
    DEFAULT_TEMPLATE = """
{{ contact_person_greeting }}：

感谢贵校报名参加{{ consultation_title }}！您的参会报名已成功确认，现将参会信息通知如下：

【咨询会信息】
- 咨询会名称：{{ consultation_title }}
- 举办时间：{{ consultation_date }}
- 举办地点：{{ consultation_location }}
- 展位号：{{ booth_number }}

{% if contact_person %}
【联系人】{{ contact_person }}
{% endif %}

请贵校参会人员提前做好准备，准时到达指定地点。如有任何问题，请及时与我们联系。

再次感谢贵校的参与和支持！

此致
敬礼

招生咨询管理系统
"""

    @classmethod
    def get_default_template(cls) -> str:
        """
        获取默认回执模板

        返回:
            str: 默认模板字符串
        """
        return cls.DEFAULT_TEMPLATE.strip()

    @classmethod
    def get_simple_template(cls) -> str:
        """
        获取简化版回执模板

        返回:
            str: 简化版模板字符串
        """
        return """
{{ contact_person_greeting }}：

您的参会报名已成功确认！

【参会信息】
咨询会：{{ consultation_title }}
时间：{{ consultation_date }}
地点：{{ consultation_location }}
展位号：{{ booth_number }}

祝参会顺利！
        """.strip()

    @classmethod
    def render(
        cls,
        template: str | None = None,
        variables: dict[str, Any] | None = None,
    ) -> str:
        """
        渲染模板

        参数:
            template (str | None): 模板字符串，默认使用默认模板
            variables (dict | None): 变量字典

        返回:
            str: 渲染后的邮件内容
        """
        from app.common.email_service import EmailService

        template = template or cls.DEFAULT_TEMPLATE
        variables = variables or {}

        return EmailService._render_template(template, variables)

    @classmethod
    def validate_template(cls, template: str) -> bool:
        """
        验证模板格式是否正确

        参数:
            template (str): 模板字符串

        返回:
            bool: 是否有效
        """
        if not template or not template.strip():
            return False

        # 检查是否有必要的占位符
        required_vars = [
            "consultation_title",
            "consultation_date",
            "consultation_location",
        ]
        for var in required_vars:
            if f"{{{{ {var}}}}}" not in template and f"{{{{{var}}}}}" not in template:
                return False

        return True
