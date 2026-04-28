# -*- coding: utf-8 -*-

from typing import Dict, List
import yaml
from string import Template
import logging

class YamlPack:
    # yaml文件全部内容
    def __init__(self, yaml_path, api_host: str, token: str):
        # yaml中的变量
        variable = {
            'host': api_host,
            'token': token
        }
        self.pass_num = 0
        self.fail_num = 0
        self.yaml_path = yaml_path
        with open(self.yaml_path, 'r', encoding="utf-8") as f:
            re = Template(f.read()).substitute(variable)
            self.data = yaml.safe_load(re)
            logging.info(f"成功读取Yaml文件: {self.yaml_path}")

    # Test目录下的全部用例
    def load_test_cases(self) -> List[Dict]:
        test_list = []
        case = self.data["Case"]
        for a in case:
            for k, v in a.items():
                if k == "Test":
                    test_list.append(v)
        return test_list

