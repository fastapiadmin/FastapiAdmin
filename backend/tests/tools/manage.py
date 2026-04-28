# -*- coding: utf-8 -*-

import logging
from typing import Dict

from common.reponse_tool import Response
from common.request_tool import Requests


class Manage:

    def __init__(self):
        pass
        

    def create_result(self, name: str, status: str = 'skip', response: str = None) -> Dict:
        """创建统一的结果对象"""
        return {
            'name': name,
            'result': status,
            'response': response
        }

    def execute_test_case(self, case: Dict) -> Dict:
        """执行测试用例"""
        try:
            # 构建请求数据
            request_data = {
                'url': case['request']['url'],
                'method': case['request']['method'],
                'data': case['request']['data'],
                'headers': case['request']['headers'],
                'data_type': case.get('type', 'json')
            }

            # 发送请求并获取响应
            response = Response().result(Requests().send_request(**request_data))
            
            # 断言
             # 情况1：如果响应体包含'isSuccess'字段（按预期格式）
            if case['expected']['isSuccess'] and  case['expected']['code'] == response['code']:
                status = 'pass'
            else:
                status = 'fail'
            
            result = self.create_result(case['name'], status, response)
            logging.info(f"用例执行完成: {case['name']}, 结果: {status}")
            
        except Exception as e:
            error_msg = f"执行用例异常: {str(e)}"
            logging.error(error_msg)
            result = self.create_result(case['name'], 'fail', error_msg)
            
        return result


