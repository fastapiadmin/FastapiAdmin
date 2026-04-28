# Auto_Test

## 项目简介

Auto_Test 是一个完全开源免费的自动化测试框架，旨在整合多种工具和技术，提供全面的API和UI自动化测试解决方案。通过使用pytest、playwright、locust、pytest-html、requests、Jenkins等技术，本项目能够帮助测试员高效地进行自动化测试，并生成详细的测试报告。支持通过Jenkins构建发送测试结果通知到邮件、钉钉、企微，方便团队成员及时了解测试状态。

## 关键特性

- **多技术整合**：结合Python、pytest、playwright等多种工具，实现API和UI自动化测试。
- **详细报告**：使用pytest-html生成美观且详细的测试报告。
- **数据处理**：利用openpyxl和pandas处理Excel数据，方便测试数据管理和结果分析。
- **通知集成**：通过DingTalk发送测试结果通知，确保团队及时了解测试状态。
- **性能测试**：利用locust进行性能测试，评估系统在高负载下的性能表现。
- **数据伪造**：借助Faker生成假数据，丰富测试场景。
- **持续集成**：通过Jenkins实现持续集成，确保项目代码始终处于良好状态。

## 项目结构

```plaintext
AUTO_TEST
├── case               # 测试数据目录
│   ├── api            # 接口测试数据目录
│   ├── locustfiles    # locust性能测试数据目录
│   └── ui             # UI测试数据目录
├── common             # 全局公共模块
├── config             # 配置文件
├── logs               # 日志目录
├── report             # 测试报告
├── testCase           # 测试用例目录
│   ├── api            # 接口测试用例目录
│   └── ui             # UI测试用例目录
├── tools              # 工具类目录
├── .env               # 环境变量配置
├── locust.conf        # locust性能测试配置文件
├── main.py            # 测试主入口
├── pytest.ini         # pytest配置文件
├── README.md          # 项目说明文档
└── requirements.txt   # 依赖包版本文件
```

## 快速开始

1.工具：

- python下载地址: <https://www.python.org/download>
- pycharm下载地址: <https://www.jetbrains.com/pycharm>

2.搭建步骤

- 2.1拉取代码
  - git clone <https://gitee.com/fastapiadmin/AutoTest.git>
  - 查看本地和远程所有分支： git branch -a
  - 切换分支：git checkout [branch-name]

- 2.2创建虚拟环境：
  - python -m venv venv
  - venv/Scripts/activate
  - 回车激活环境

- 2.3安装项目依赖包
  - pip install -r requirements.txt
  - pip install -r requirements.txt --upgrade

- 2.4运行项目
  - 运行前检查config目录中Config.ini文件是否配置正确
  - python main.py

- 2.5ui录制脚本
  - playwright codegen

  - 如果没有找到浏览器驱动则执行下方,一次会下载三个浏览器，chromium、firefox、webkit
    playwright install
  
  - 或者指定下载浏览器
    playwright install chromium
    playwright install firefox
    playwright install webkit
  
- 性能测试
  - https://docs.locust.io/en/stable/api.html

## 🎨 社区交流

| 群组二维码 | 微信支付二维码 |
| --- | --- |
| ![群组二维码](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/group.jpg) | ![微信支付二维码](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/wechatPay.jpg) |