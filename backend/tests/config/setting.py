# -*- coding: utf-8 -*-#

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

from tools.random_tool import ContextPack

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file='.env',
    env_file_encoding='utf-8',
    extra='ignore'
  )

  BANNER: str = """
    __    _ _  _____  ___  _____  ____  __  _____ 
   / /\  | | |  | |  / / \  | |  | |_  ( (`  | |  
  /_/--\ \_\_/  |_|  \_\_/  |_|  |_|__ _)_)  |_|  
  """
  # ===================公共配置======================
  # 项目的根目录
  BASE_PATH: Path = Path(__file__).parent.parent
  # 用例所需测试文件路径
  CASE_PATH: Path = BASE_PATH / "case"
  # log路径
  LOG_PATH: Path = BASE_PATH / "logs" / (ContextPack().get_day_time + '.log')
  # 项目测试报告
  REPORT_PATH: Path = BASE_PATH / "reports"
  # 项目测试报告路径
  HTML_REPORT_PATH: Path = REPORT_PATH / (ContextPack().get_day_time + '.html')
  # api数据路径
  API_EXCEL_FILE: Path = CASE_PATH / "api" / "case.xlsx"
  API_YAML_PATH: Path = CASE_PATH / "api" / 'case.yaml'
  # UI截图路径
  UI_IMG_PATH: Path = REPORT_PATH / "img"

  # ===================环境配置======================
  TEST_TYPE: str
  ENVIRONMENT: str
  ENVIRONMENT_HOST: str
  ENVIRONMENT_TOKEN: str

  # ===================测试人员======================
  TESTER: str

  # ===================公共配置======================
  DELETE_ON_OFF: bool
  EMAIL_ON_OFF: bool
  DINGDING_ON_OFF: bool
  JENKINS_URL: str
  REPORT_URL: str

  # ===================邮件配置======================
  EMAIL_SMTP_SERVER: str
  EMAIL_SENDER: str
  EMAIL_PASSWORD: str
  EMAIL_RECEIVER: str

  # ===================钉钉配置======================
  DINGDING_SECRET: str
  DINGDING_WEBHOOK: str
  DINGDING_AT_MOBILES: list[str]

  # ===================浏览器配置======================
  BROWSER_TYPE: str

  # ===================企业微信配置======================
  QIWEI_ON_OFF: bool
  WEBHOOK_URL: str

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()