# -*- coding: utf-8 -*-

import pytest
from playwright.sync_api import Page
from case.ui.pages.base_page import BasePage
from typing import Dict, Any


@pytest.mark.usefixtures('init_session')
class TestUI:
    
    # 定义测试数据
    TEST_DATA = [{参数化1},{参数化2}]

    @pytest.mark.ui
    @pytest.mark.parametrize("test_data", TEST_DATA)
    def test_login_scenarios(self, init_session: Page, test_data: Dict[str, Any]):
        """参数化测试不同的登录场景"""
        emposat_page = BasePage(init_session)

        login_result = emposat_page.login(test_data=test_data)
        assert login_result == True, "登录失败"

        logout_result = emposat_page.logout()
        assert logout_result == True, "退出登录失败"
