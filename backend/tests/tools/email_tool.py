# -*- coding: utf-8 -*-

import smtplib
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging


class EmailPack:
    # 初始化发件人，密码，收件人列表
    def __init__(self, fromaddr: str, password: str, toaddrs: list, server_host: str):
        """
        :param REPORT_END_PATH:
        """
        self.fromaddr = fromaddr
        self.password = password
        self.toaddrs = toaddrs
        self.server_host = server_host

        self.server = smtplib.SMTP(self.server_host)
        self.message = MIMEMultipart()

    # 设置发件人名称，主题，内容，附件
    def _set_message(self, name: str, title: str, content: str, filelist: list):
        """
        :param name:
        :param title:
        :param content:
        :param filelist:
        :return:
        """
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.message['From'] = Header(f"{name}<{self.fromaddr}>", 'utf-8')  # 发件人名称和地址
        self.message['Subject'] = Header(title + "_" + tm, 'utf-8')  # 邮件主题
        self.message.attach(MIMEText(content))  # 邮件内容
        if filelist is not None:  # 邮件附件
            for file in filelist:
                fileApart = MIMEApplication( open(file, 'rb').read(), file.split('.')[-1])
                fileApart.add_header('Content-Disposition', 'attachment', filename=file.split("\\")[-1])
                self.message.attach(fileApart)

    # 发送邮件
    def _send_message(self):
        """
        :return:
        """
        try:
            self.server.login(self.fromaddr, self.password)
            self.server.sendmail(self.fromaddr, self.toaddrs, self.message.as_string())
            logging.info(f'【邮件发送成功！收件人：{self.toaddrs}】')
            self.server.quit()
        except smtplib.SMTPException as e:
            logging.error(f'【邮件发送异常！{e}】')

    # 默认发送邮件
    def send_default_email(self, title: str, environment: str, tester: str, total: int, pass_num: int, fail_num: int, error_num: int, skip_num: int, rate: str, duration: str, reprot_url: str, jenkins_url: str, report_path: list):
        """
        :rtype: object
        :return:
        """

        self._set_message(
            name="自动化测试",
            title=f'{title}测试执行完毕提醒！',
            content=f'''
                各位同事, 大家好:
                自动化用例执行完成，执行结果如下:
                    **********************************
                    执行环境: {environment}
                    执行人员: {tester} 
                    运行总数: {total}
                    通过: {pass_num}
                    失败: {fail_num}
                    异常: {error_num}
                    跳过: {skip_num}
                    成功率: {rate}
                    总耗时: {duration}
                    报告详情: [点击查看]({reprot_url})
                    **********************************
                    jenkins地址：{jenkins_url}
                    详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。
                    ''',
            filelist=[report_path]
        )
        self._send_message()

