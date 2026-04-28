

# -*- coding: utf-8 -*-#

# 企业微信发送消息模块
import requests
import json
from typing import Any, List, Optional


class QiWeiPack:
    """
    企业微信机器人消息发送封装类
    """

    def __init__(self, webhook_url: str):
        """
        初始化企业微信机器人
        :param webhook_url: 企业微信机器人的webhook地址
        """
        self.webhook_url = webhook_url
        self.headers = {"Content-Type": "application/json"}

    def _send_request(self, data: dict) -> dict:
        """
        发送请求到企业微信API
        :param data: 消息数据
        :return: 响应结果
        """
        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(data), 
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"发送企业微信消息失败: {str(e)}")

    def send_text(self, content: str, mentioned_list: Optional[List[str]] = None, mentioned_mobile_list: Optional[List[str]] = None) -> dict:
        """
        发送文本消息
        :param content: 文本内容
        :param mentioned_list: @的用户列表，如["user1", "user2"]
        :param mentioned_mobile_list: @的手机号列表，如["13800138000"]
        :return: 响应结果
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        if mentioned_list:
            data["text"]["mentioned_list"] = mentioned_list
        if mentioned_mobile_list:
            data["text"]["mentioned_mobile_list"] = mentioned_mobile_list
        
        return self._send_request(data)

    def send_markdown(self, content: str) -> dict:
        """
        发送markdown消息
        :param content: markdown内容
        :return: 响应结果
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        return self._send_request(data)

    def send_image(self, base64: str, md5: str) -> dict:
        """
        发送图片消息
        :param base64: 图片base64编码
        :param md5: 图片md5值
        :return: 响应结果
        """
        data = {
            "msgtype": "image",
            "image": {
                "base64": base64,
                "md5": md5
            }
        }
        return self._send_request(data)

    def send_news(self, articles: List[dict]) -> dict:
        """
        发送图文消息
        :param articles: 图文列表，每个元素包含title、description、url、picurl字段
        :return: 响应结果
        """
        data = {
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }
        return self._send_request(data)

    def send_file(self, media_id: str) -> dict:
        """
        发送文件消息
        :param media_id: 文件媒体ID（需要先上传文件获取）
        :return: 响应结果
        """
        data = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        return self._send_request(data)

    def send_taskcard(self, title: str, description: str, url: str, btn_json_list: List[dict]) -> dict:
        """
        发送任务卡片消息
        :param title: 标题
        :param description: 描述
        :param url: 点击卡片跳转的URL
        :param btn_json_list: 按钮列表
        :return: 响应结果
        """
        data = {
            "msgtype": "taskcard",
            "taskcard": {
                "title": title,
                "description": description,
                "url": url,
                "btn_json_list": btn_json_list
            }
        }
        return self._send_request(data)

    def send_test_report(self, title: str, environment: str, tester: str, total: int, pass_num: int, 
                         fail_num: int, error_num: int, skip_num: int, rate: str, duration: str, 
                         report_url: str, jenkins_url: str) -> dict:
        """
        发送测试报告通知
        :param title: 测试标题
        :param environment: 执行环境
        :param tester: 执行人员
        :param total: 运行总数
        :param pass_num: 通过数量
        :param fail_num: 失败数量
        :param error_num: 异常数量
        :param skip_num: 跳过数量
        :param rate: 成功率
        :param duration: 运行时间
        :param report_url: 报告地址
        :param jenkins_url: Jenkins地址
        :return: 响应结果
        """
        # 企业微信markdown支持的颜色有限，这里使用emoji和加粗来突出显示
        content = (
            f"## {title}测试执行完毕提醒\n\n" +
            "📢 **测试执行完成**\n\n" +
            "---\n\n" +
            f"**执行环境：** {environment}\n\n" +
            f"**执行人员：** {tester}\n\n" +
            "---\n\n" +
            f"**运行总数：** {total}\n\n" +
            f"**通过数量：** ✅ {pass_num}\n\n" +
            f"**失败数量：** ❌ {fail_num}\n\n" +
            f"**异常数量：** ⚠️ {error_num}\n\n" +
            f"**跳过数量：** ⏭️ {skip_num}\n\n" +
            f"**成功率：** {rate}\n\n" +
            f"**运行时间：** {duration}\n\n" +
            f"**报告详情：** [点击查看]({report_url})\n\n" +
            f"**构建地址：** [点击查看]({jenkins_url})\n\n" +
            "详细情况可登录Jenkins平台查看，非相关负责人员可忽略此消息。谢谢。"
        )
        
        return self.send_markdown(content)

    