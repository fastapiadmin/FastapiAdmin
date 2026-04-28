# -*- coding: utf-8 -*-

import logging
import requests

class Response:
    def __init__(self):
        pass

    def result(self, res: requests.Response) -> dict:
        """
        :param res: requests响应对象
        :return: 格式化后的响应字典
        """
        try:
            response_dicts = dict()
           
            # 响应状态码
            response_dicts['code'] = res.status_code
            
            # 响应body
            response_body = res.json()

             # 确保响应体是字典格式
            if isinstance(response_body, dict):
                response_dicts['body'] = response_body
            
            # 响应秒时间
            response_dicts['time_total'] = res.elapsed.total_seconds()  # 秒为单位 

            logging.info(f"【请求响应结果为: {response_dicts}】")
            return response_dicts
        except Exception as e:
            logging.error(f"响应结果处理异常：{e}")
