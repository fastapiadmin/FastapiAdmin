# -*- coding: utf-8 -*-

import requests
import logging

class Requests:
    def __init__(self):
        """
        单例模式保证测试过程中使用的都是一个session对象
        """
        self.session = requests.Session()

    def send_request(self,url: str, method: str, data_type: str, headers: dict = None, data: dict = None):
        """
        :param url: 请求url
        :param method: 请求方法
        :param data_type: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数), json(一般用于json类型请求参数)
        :param headers: 请求头
        :param data: 参数数据，默认等于None
        :return: 返回res对象
        """
        res = None
        try:
            logging.info(f"""
            【请求地址】Url: {url}
            【请求类型】Method: {method}
            【请求头】Headers: {headers}
            【请求数据】Data: {data}
            """)
            if data_type == 'params':
                res = self.session.request(method=method, url=url, params=data, headers=headers)
            elif data_type == 'data':
                res = self.session.request(method=method, url=url, data=data, headers=headers)
            elif data_type == 'json':
                res = self.session.request(method=method, url=url, json=data, headers=headers)
            elif data_type == 'file':
                res = self.session.request(method=method, url=url, files=data, headers=headers)
            else:
                logging.error('parametric_key为params、json、data、file, 不支持其他类型')
        except Exception as e:
            logging.error(f"发送请求异常:{e}")
        return res
