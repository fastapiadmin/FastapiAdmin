# -*- coding: utf-8 -*-

import pytest
from config.setting import settings

# 获取Jenkins选项参数(切记参数名称不可以使用中文)
# import os
# TEST_TYPE = os.environ['TESTTYPE']
# ENVIRONMENT: str = os.environ['ENVIRONMENT']
# API_HOST: str = os.environ['APIHOST']
# TESTER: str = os.environ['TESTER']

args = [
    '-sv',
    f'--html={settings.HTML_REPORT_PATH}',
    '--self-contained-html',  # 静态html, 不需要额外的资源文件
    f'--log-file={settings.LOG_PATH}',
    '-W', 'ignore:Module already imported:pytest.PytestWarning'
]

if __name__ == '__main__':
    # 执行测试
    pytest.main(args)
