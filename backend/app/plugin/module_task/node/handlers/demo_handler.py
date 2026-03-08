"""
示例处理器模块

提供简单的示例方法供节点执行函数调用
"""

from datetime import datetime


def demo_handler(*args, **kwargs) -> dict:
    """示例处理器"""
    return {
        "message": "Hello from demo_handler!",
        "args": args,
        "kwargs": kwargs,
        "time": datetime.now().isoformat(),
    }


def process_data(data: list, operation: str = "sum") -> dict:
    """
    简单数据处理

    operation: sum, avg, max, min, count
    """
    if not data:
        return {"error": "数据为空"}

    if operation == "sum":
        result = sum(data)
    elif operation == "avg":
        result = sum(data) / len(data)
    elif operation == "max":
        result = max(data)
    elif operation == "min":
        result = min(data)
    elif operation == "count":
        result = len(data)
    else:
        return {"error": f"不支持的操作: {operation}"}

    return {"operation": operation, "result": result}
