# -*- coding: utf-8 -*-

from typing import Dict, Any
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
    
    def login(self, test_data: Dict[str, Any]) -> bool:
        # 设置页面加载超时
        self.page.set_default_timeout(30000)
        
        # 访问登录页面并等待页面完全加载
        self.page.goto(test_data["url"])
        self.page.wait_for_load_state("networkidle")  # 等待网络活动空闲
        
        # 等待用户名输入框可见且可交互
        username_input = self.page.get_by_role("textbox", name="用户名")
        username_input.wait_for(state="visible", timeout=10000)
        username_input.click()
        username_input.fill(test_data["username"])
        
        # 等待密码输入框可见且可交互
        password_input = self.page.get_by_role("textbox", name="请输入登录密码")
        password_input.wait_for(state="visible", timeout=10000)
        password_input.click()
        password_input.fill(test_data["password"])
        
        # 等待登录按钮可见且可交互
        login_button = self.page.get_by_role("button", name="登录")
        login_button.wait_for(state="visible", timeout=10000)
        # 使用click()方法本身会等待元素可交互，不需要单独检查enabled状态
        login_button.click()
        
        # 等待登录后页面加载和弹窗出现
        self.page.wait_for_load_state("networkidle")
        
        # 等待SaaS系统使用引导文本出现
        self.page.wait_for_selector("text=SaaS系统使用引导", timeout=15000)
        expect(self.page.get_by_text("SaaS系统使用引导")).to_be_visible()
        expect(self.page.get_by_text("登录成功")).to_be_visible()
        
        # 等待关闭按钮可见且可交互
        close_button = self.page.get_by_role("button", name="Close")
        close_button.wait_for(state="visible", timeout=10000)
        # 使用click()方法本身会等待元素可交互，不需要单独检查enabled状态
        close_button.click()

        # 关闭登录成功提示
        self.page.locator(".el-icon.el-notification__closeBtn > svg").click()
        
        # 等待弹窗关闭
        self.page.wait_for_selector("text=SaaS系统使用引导", state="hidden", timeout=5000)

        return True

    def logout(self) -> bool:
        # 等待用户名显示
        expect(self.page.get_by_text("涛")).to_be_visible(timeout=20000)
        self.page.get_by_text("涛").click()
        # 等待退出登录选项显示
        self.page.wait_for_selector("text=退出登录", state="visible", timeout=10000)
        
        expect(self.page.get_by_text("退出登录")).to_be_visible(timeout=10000)
        self.page.get_by_text("退出登录").click()
        # 等待确认对话框显示
        self.page.wait_for_selector("text=确定要退出登录吗？", state="visible", timeout=10000)

        expect(self.page.get_by_text("确定要退出登录吗？")).to_be_visible(timeout=10000)
        expect(self.page.get_by_role("button", name="确认")).to_be_visible(timeout=10000)
        self.page.get_by_role("button", name="确认").click()
        # 等待退出成功提示显示
        self.page.wait_for_selector("text=退出成功", state="visible", timeout=10000)

        expect(self.page.get_by_text("退出成功")).to_be_visible(timeout=10000)
        # 关闭退出成功提示
        self.page.get_by_role("img").nth(4).click()

        return True
