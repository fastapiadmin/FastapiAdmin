# -*- coding: utf-8 -*-

import pytest
import logging
from typing import Dict
from config.setting import settings

from tools.excel_tool import ExcelPack
from tools.yaml_tool import YamlPack
from tools.manage import Manage

manage = Manage()
excel = ExcelPack(file_name=settings.API_EXCEL_FILE, api_host=settings.ENVIRONMENT_HOST, token=settings.ENVIRONMENT_TOKEN)
yaml = YamlPack(yaml_path=settings.API_YAML_PATH, api_host=settings.ENVIRONMENT_HOST, token=settings.ENVIRONMENT_TOKEN)


class TestExcel:

    @pytest.mark.parametrize('case', excel.load_test_cases(), ids=lambda x: x['name'])
    def test_excel_api(self, case: Dict) -> None:
        """Excel数据驱动的API测试类"""
        logging.info(f"开始执行用例: {case['name']}")

        # 检查是否需要执行
        if str(case['run']).lower() != 'yes':
            logging.info(f"跳过用例: {case['name']}")
            excel.write_to_excel(row=case['row'], result=manage.create_result(case['name'], 'skip'))
            pytest.skip()

        # 执行测试用例
        result = manage.execute_test_case(case)

        # 写入结果
        excel.write_to_excel(row=case['row'], result=result)

        # 断言结果
        assert result['result'] == 'pass', (
            f"用例执行失败: {case['name']}\n"
            f"请求信息: {case['request']}\n"
            f"期望结果: {case['expected']}\n"
            f"实际结果: {result['response']}"
        )

    @pytest.mark.parametrize('case', yaml.load_test_cases(), ids=lambda x: x['name'])
    def test_yaml_api(self, case: Dict) -> None:
        """Yaml数据驱动的API测试类"""
        logging.info(f"开始执行用例: {case['name']}")

        # 检查是否需要执行
        if not case['run']:
            logging.info(f"跳过用例: {case['name']}")
            pytest.skip()

        # 执行测试用例
        result = manage.execute_test_case(case)

        # 断言结果
        assert result['result'] == 'pass', (
            f"用例执行失败: {case['name']}\n"
            f"请求信息: {case['request']}\n"
            f"期望结果: {case['expected']}\n"
            f"实际结果: {result['response']}"
        )
