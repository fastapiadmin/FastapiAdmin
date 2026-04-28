# -*- coding: utf-8 -*-

import base64
import time
import logging
import datetime
import shutil
import pytest
from pytest_metadata.plugin import metadata_key
from _pytest.terminal import TerminalReporter

from config.setting import settings
from tools.email_tool import EmailPack
from tools.dingding_tool import DingTalkPack
from tools.qiwei_tool import QiWeiPack

# 常量定义
TEST_TYPE: str = settings.TEST_TYPE
ENVIRONMENT: str = settings.ENVIRONMENT
TESTER: str = settings.TESTER

# 状态常量
success = "✓"
fail = "✗"

# 全局page对象，用于在整个测试会话中共享
GLOBAL_PAGE = None

"""
module级别的测试初始化和结果收集
class级别的测试初始化和结果收集
function级别的测试初始化和结果收集
"""
@pytest.fixture(scope="session", autouse=True)
def init_session():
    """会话级别的测试初始化和结果收集 - 使用Playwright，确保唯一驱动实例"""
    if TEST_TYPE not in ['API', 'UI']:
        raise ValueError("请输入正确的自动化测试类型['API','UI']")
    if settings.DELETE_ON_OFF == 'True':
        if settings.REPORT_PATH.exists():
            shutil.rmtree(settings.REPORT_PATH)
        logging.info("历史报告数据清理完成")
    logging.info(
        f"{settings.BANNER}\n"
        f"开始执行 {TEST_TYPE} 自动化测试\n"
        f"测试环境: {ENVIRONMENT}\n"
        f"测试人员: {TESTER}"
    )
    from playwright.sync_api import sync_playwright
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir="./report/videos/", viewport={"width": 1920, "height": 1080}) # 生成适配视频
    page = context.new_page()
    # 更新全局page对象
    global GLOBAL_PAGE
    GLOBAL_PAGE = page
    logging.info(f"{success} ==> Playwright 浏览器实例初始化完成")
    # 返回page对象供测试用例使用
    yield page
    # 清理资源
    try:
        context.close()
        browser.close()
        playwright.stop()
        logging.info(f"{success} ==> Playwright 资源已全部释放")
    except Exception as e:
        logging.error(f"{fail} ==> Playwright 资源释放失败: {str(e)}")
    else:
        logging.info(f"========== {TEST_TYPE} 自动化测试结束 ==========")

def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: int, config: pytest.Config):
    """收集终端测试结果"""
    stats = terminalreporter.stats
    result = {
        'total': terminalreporter._numcollected,
        'passed': len(stats.get('passed', [])),
        'failed': len(stats.get('failed', [])),
        'skipped': len(stats.get('skipped', [])),
        'error': len(stats.get('error', [])),
        'success_rate': f"{((len(stats.get('passed', [])) / terminalreporter._numcollected * 100) if terminalreporter._numcollected else 0):.2f}%",
        'duration': f'{round(time.time() - terminalreporter._sessionstarttime, 2)}秒',
        'reprot_url': settings.REPORT_URL,
        'jenkins_url': settings.JENKINS_URL
    }
    
    logging.info(f"总用例数: {result['total']} | 通过: {result['passed']}| 失败: {result['failed']} | 跳过: {result['skipped']} | 错误: {result['error']} | 成功率: {result['success_rate']} | 总耗时: {result['duration']}")

    # 发送邮件
    if settings.EMAIL_ON_OFF:
        EmailPack(
            fromaddr=settings.EMAIL_SENDER,
            password=settings.EMAIL_PASSWORD,
            toaddrs=[settings.EMAIL_RECEIVER],
            server_host=settings.EMAIL_SMTP_SERVER
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
        # 调整参数名以匹配企业微信工具的要求
        qiwei_result = {
            'total': result['total'],
            'pass_num': result['passed'],
            'fail_num': result['failed'],
            'error_num': result['error'],
            'skip_num': result['skipped'],
            'rate': result['success_rate'],
            'duration': result['duration'],
            'report_url': result['reprot_url'],  # 修正拼写错误
            'jenkins_url': result['jenkins_url']
        }
        QiWeiPack(settings.WEBHOOK_URL).send_test_report(
            title=TEST_TYPE,
            environment=ENVIRONMENT,
            tester=TESTER,
            **qiwei_result
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
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    extras = getattr(report, 'extras', [])
    extras.append(pytest_html.extras.url(str(settings.LOG_PATH), name="查看运行日志"))
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            # 使用全局page对象
            base64_img = screenshot_base64()
            if file_name:
                html = """
                    <div>
                        <img src="data:image/png;base64,%s" alt="screenshot" style="width:460px;height:230px;" align="right" onclick="window.open(this.src)"/>
                    </div>
                """ % base64_img
                extras.append(pytest_html.extras.html(html))
        report.extras = extras
        report.description = str(item.function.__doc__)

def screenshot_base64():
    """获取当前页面的截图base64编码，使用全局page对象"""
    # 生成简洁的截图文件名（年月日时分秒格式）
    settings.UI_IMG_PATH.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = settings.UI_IMG_PATH / f"{timestamp}.png"
    # 使用全局page对象
    global GLOBAL_PAGE
    page = GLOBAL_PAGE
    # 检查page对象是否存在
    if page and hasattr(page, 'screenshot'):
        try:
            screenshot_bytes = page.screenshot(path=screenshot_path)
            logging.info(f"{success} ==> 保存失败截图: {screenshot_path}")
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        except Exception as e:
            logging.error(f"{fail} ==> 截图失败: {str(e)}")
            return ''
    