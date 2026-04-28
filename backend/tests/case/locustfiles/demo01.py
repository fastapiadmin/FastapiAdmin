import time
from locust import HttpUser, task, between, User
from locust.runners import MasterRunner

from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("开始监听")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("结束监听")

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("我在master节点上")
    else:
        print("我在worker节点或独立节点上")

class QuickstartUser(HttpUser):
    # 例如，让每个用户在每次任务执行之间等待0.5到10秒：
    wait_time = between(0.5, 10)

    # 例如，下一个用户类会睡一秒，然后两秒，再三秒，依此类推。
    last_wait_time = 0

    def wait_time(self):
        self.last_wait_time += 1
        return self.last_wait_time

    # @task 会有一个可选的权重参数，可以用来指定任务的执行比率。在 以下示例，任务2被选中的概率是任务1的两倍：
    @task(3)
    def task1(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(6)
    def task2(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)
    
    
    @task
    def my_task(self):
        with self.client.get("/", catch_response=True) as response:
            if response.text != "Success":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")
            elif response.status_code == 404:
                raise RescheduleTask()

    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})

# 例如，假设我们有一个WebUser类和一个MobileUser类，我们想让MobileUser类的用户权重为1，而WebUser类的用户权重为3。
class WebUser(User):
    weight = 3
    ...

class MobileUser(User):
    weight = 1
    ...