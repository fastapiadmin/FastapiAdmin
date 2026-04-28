# 在最佳情况下（在 -loop 内执行小请求），单个 Locust 进程（限制在一个 CPU 核心）
# 使用 FastHttpUser 可以每秒处理大约 16000 个请求，使用 HttpUser 可以执行 4000
#  个请求（测试于 2021 年 M1 MacBook Pro 和 Python 3.11 上）

from locust import TaskSet, task, HttpUser, run_single_user, FastHttpUser
from locust.clients import ResponseContextManager
from locust.runners import logger
from locust import HttpUser, task, between

class Task(TaskSet):
    tasks = {ThreadPage:15, write_post:1}
    @tag('thread')
    @task(3)
    def demo_api(self):
        # 基于注释中的接口信息设置请求参数
        payload = {}
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "token": "xxxx"
        }

        path = "/gateway/xxx"
        logger.info(f"请求路径 {path}")
        with self.client.post(path, json=payload, headers=headers, catch_response=True) as res:
            res: ResponseContextManager
            if res.status_code != 200:
                # 输出请求的完整 URL 和状态码
                logger.error(f"请求失败. 接口地址: {res.request.url}, 状态码: {res.status_code}")
                # 输出响应文本
                logger.error(f"响应文本: {res.text}")
                # 标记请求为失败
                res.failure(res.text)
            else:
                # 检查响应内容是否包含预期的数据结构
                try:
                    response_json = res.json()
                    if not response_json:
                        res.failure("响应体为空")
                except ValueError:
                    res.failure("响应体不是有效的 JSON 格式")

    

    def on_start(self):
        logger.info('s'*10 + '测试开始' + 's'*10)
        
    def on_stop(self):
        logger.info('s'*10 + '测试结束' + 's'*10)

# class Test(HttpUser):
class Test(FastHttpUser):
    wait_time = between(1, 5)

    # 根据注释中的接口地址更新host配置
    host = 'https://xxx.com'
    tasks = [Task, ]

    @task
    def t(self):
        with self.rest("POST", "/", json={"foo": 1}) as resp:
            if resp.js is None:
                pass # no need to do anything, already marked as failed
            elif "bar" not in resp.js:
                resp.failure(f"'bar' missing from response {resp.text}")
            elif resp.js["bar"] != 42:
                resp.failure(f"'bar' had an unexpected value: {resp.js['bar']}")

if __name__ == '__main__':
    # 修复变量名错误，应该是Test类而不是test
    run_single_user(Test)

    # 启动 Locust 测试
    # locust -f locust.py
