"""
工作流编排子包（plugin.module_task.workflow）：

- ``definition``: 工作流定义（画布 CRUD、发布、执行 API）
- ``node_type``: 编排节点类型（palette / 与 task_node 分离）
- ``engine``: 拓扑分层并行执行引擎

动态路由仍统一挂在 ``/task`` 下（见各子包 ``controller.py`` 的 ``prefix``）。
"""
