# -*- coding: utf-8 -*-

import datetime
import time
import os
import shutil
import pytest
from _pytest.terminal import TerminalReporter
import pytest_html
import pytest_html.extras
from pytest_metadata.plugin import metadata_key
import logging

from config.setting import settings
from tools.email_tool import EmailPack
from tools.dingding_tool import DingTalkPack
from tools.qiwei_tool import QiWeiPack

# 常量定义
TEST_TYPE: str = settings.TEST_TYPE
ENVIRONMENT: str = settings.ENVIRONMENT
TESTER: str = settings.TESTER

"""
module级别的测试初始化和结果收集
class级别的测试初始化和结果收集
function级别的测试初始化和结果收集
"""
@pytest.fixture(scope="session", autouse=True)
def init_session():
    """会话级别的测试初始化和结果收集"""
    if TEST_TYPE not in ['API', 'UI']:
        raise ValueError("请输入正确的自动化测试类型['API','UI']")
    if settings.DELETE_ON_OFF == 'True':
        if os.path.exists(settings.REPORT_PATH):
            shutil.rmtree(settings.REPORT_PATH)
        logging.info("历史报告数据清理完成")
    logging.info(f"{settings.BANNER}\n"
                f"开始执行 {TEST_TYPE} 自动化测试\n"
                f"测试环境: {ENVIRONMENT}\n"
                f"测试人员: {TESTER}")
    yield
    logging.info(f"========== {TEST_TYPE} 自动化测试结束 ==========")

def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: int, config: pytest.Config):
    """收集终端测试结果"""
    stats = terminalreporter.stats
    result = {
        'total': terminalreporter._numcollected,
        'pass_num': len(stats.get('passed', [])),
        'fail_num': len(stats.get('failed', [])),
        'skip_num': len(stats.get('skipped', [])),
        'error_num': len(stats.get('error', [])),
        'rate': f"{((len(stats.get('passed', [])) / terminalreporter._numcollected * 100) if terminalreporter._numcollected else 0):.2f}%",
        'duration': f'{round(time.time() - terminalreporter._sessionstarttime, 2)}秒',
        'reprot_url': settings.REPORT_URL,
        'jenkins_url': settings.JENKINS_URL
    }
    
    logging.info(f"总用例数: {result['total']} | 通过: {result['pass_num']}| 失败: {result['fail_num']} | 跳过: {result['skip_num']} | 错误: {result['error_num']} | 成功率: {result['rate']} | 总耗时: {result['duration']}")

    # 发送邮件
    if settings.EMAIL_ON_OFF:
        EmailPack(
            fromaddr=settings.EMAIL_SENDER,
            password=settings.EMAIL_PASSWORD,
            toaddrs=[settings.EMAIL_RECEIVER],
            server_host=settings.EMAIL_SMTP_SERVER,
        ).send_default_email(
            title=TEST_TYPE,
            environment=ENVIRONMENT,
            tester=TESTER,
            **result
        )
    
    # 发送钉钉消息
    if settings.DINGDING_ON_OFF:
        DingTalkPack(settings.DINGDING_WEBHOOK, settings.DINGDING_SECRET).send_dingding(
            title=TEST_TYPE,
            environment=ENVIRONMENT,
            tester=TESTER,
            **result
        )
        
    # 发送企业微信消息
    if settings.QIWEI_ON_OFF:
        QiWeiPack(settings.WEBHOOK_URL).send_test_report(
            title=TEST_TYPE,
            environment=ENVIRONMENT,
            tester=TESTER,
            **result
        )

def pytest_html_report_title(report):
    """设置报告标题"""
    report.title = f"{TEST_TYPE}自动化测试报告"

def pytest_configure(config: pytest.Config):
    """测试配置"""
    config.stash[metadata_key].update({
        "项目名称": f"{TEST_TYPE} 自动化测试",
        "测试类型": TEST_TYPE,
        "测试环境": ENVIRONMENT,
        "测试人员": TESTER,
        "开始时间": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call: pytest.CallInfo):
    """处理测试报告"""
    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    
    if report.when == "call" and report.failed:
        extras = getattr(report, 'extras', [])
        if os.path.exists(settings.LOG_PATH):
            extras.append(pytest_html.extras.url(settings.LOG_PATH, name="查看详细日志"))
        report.extras = extras

