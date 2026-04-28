# -*- coding: utf-8 -*-#

# 钉钉发送消息模块
from typing import Any
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink

class DingTalkPack:

    def __init__(self, webhook: str, secret: str, at_mobiles: list = None):

        self.webhook=webhook
        self.secret=secret
        self.at_mobiles=at_mobiles
        
        self.ding_news = DingtalkChatbot(webhook=self.webhook, secret=self.secret, pc_slide=False, fail_notice=False)

    def send_text(self, msg: str, mobiles: list = None) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 用户电话
        :return:
        """
        if not mobiles:
            self.ding_news.send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.ding_news.send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(self, title: str, text: str, message_url: str, pic_url: str) -> None:
        """
        发送link通知
        :return:
        """
        try:
            self.ding_news.send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)
        except Exception:
            raise

    def send_markdown(self, title: str, msg: str, mobiles: list = None) -> None:
        """
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """
        if mobiles is None:
            self.ding_news.send_markdown(title=title, text=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.ding_news.send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def feed_link(self, title: str, message_url: str, pic_url: str) -> Any:
        """
        发送link类型
        :param title:
        :param message_url:
        :param pic_url:
        :return:
        """
        return FeedLink(title=title, message_url=message_url, pic_url=pic_url)

    def send_feed_link(self, *arg) -> None:
        """
        发送feedlink类型
        :param arg:
        :return:
        """
        try:
            self.ding_news.send_feed_card(list(arg))
        except Exception:
            raise

    def send_dingding(self, title, environment, tester, total, pass_num, fail_num, error_num, skip_num, rate, duration, reprot_url, jenkins_url):
        """
        发送钉钉通知
        :return:
        """
        self.ding_news.send_markdown(
            title=f'【{title}测试执行完毕提醒',
            text=f"<font color=\'#FFA500\'>[通知] </font>测试执行完成 \n\n --- \n\n" +
                 "执行环境：<font color=\"#1d953f\">%s </font>" % environment + "\n\n" +
                 "执行人员：<font color=\"#f2eada\">@%s</font>" % tester + "\n\n --- \n\n" +
                 "运行总数：<font color=\"#d71345\">%s </font>" % total + "\n\n" +
                 "通过数量：<font color=\"#1d953f\">%s </font>" % pass_num + "\n\n" +
                 "失败数量：<font color=\"#c63c26\">%s </font>" % fail_num + "\n\n" +
                 "异常数量：<font color=\"#fdb933\">%s </font>" % error_num + "\n\n" +
                 "跳过数量：<font color=\"#2585a6\">%s </font>" % skip_num + "\n\n" +
                 "成功率为：<font color=\"#1d953f\">%s </font>" % rate + "\n\n" +
                 "运行时间：<font color=\"#464547\">%s </font>" % duration + "\n\n" +
                 "报告详情：[点击查看](%s)" % reprot_url + "\n\n" +
                 "构建地址：[点击查看](%s) 详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。" % jenkins_url ,
            at_mobiles=self.at_mobiles
        )



