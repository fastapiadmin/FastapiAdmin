"""
节点执行处理器模块

提供各种封装好的方法供节点执行函数调用

使用方法:
    在节点执行函数中，所有工具函数已经自动加载到全局命名空间，
    可以直接使用，无需导入。
    
    例如:
    def handler(*args, **kwargs):
        log_info("任务开始")
        result = http_get("https://api.example.com")
        log_info(f"请求结果: {result}")
        return result
"""

# 这个模块的主要作用是提供文档说明
# 实际的功能函数在 context.py 中定义，并通过 NodeExecutionContext 注入到执行环境

__all__ = []
