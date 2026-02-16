from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.utils.cron_util import CronUtil
from app.utils.excel_util import ExcelUtil

from .crud import JobCRUD, JobLogCRUD
from .schema import (
    JobCreateSchema,
    JobLogOutSchema,
    JobLogQueryParam,
    JobOutSchema,
    JobQueryParam,
    JobUpdateSchema,
)
from .tools.ap_scheduler import SchedulerUtil


class JobService:
    """
    定时任务管理模块服务层
    """

    @classmethod
    async def get_job_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取定时任务详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 定时任务ID

        返回:
        - Dict: 定时任务详情字典
        """
        obj = await JobCRUD(auth).get_obj_by_id_crud(id=id)
        return JobOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_job_list_service(
        cls,
        auth: AuthSchema,
        search: JobQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取定时任务列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (JobQueryParam | None): 查询参数模型
        - order_by (list[dict[str, str]] | None): 排序参数列表

        返回:
        - List[Dict]: 定时任务详情字典列表
        """
        obj_list = await JobCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        return [JobOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def create_job_service(cls, auth: AuthSchema, data: JobCreateSchema) -> dict:
        """
        创建定时任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (JobCreateSchema): 定时任务创建模型

        返回:
        - Dict: 定时任务详情字典
        """
        exist_obj = await JobCRUD(auth).get(name=data.name)
        if exist_obj:
            raise CustomException(msg="创建失败，该定时任务已存在")

        obj = await JobCRUD(auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败，该数据定时任务不存在")
        SchedulerUtil().add_job(job_info=obj)
        return JobOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_job_service(cls, auth: AuthSchema, id: int, data: JobUpdateSchema) -> dict:
        """
        更新定时任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 定时任务ID
        - data (JobUpdateSchema): 定时任务更新模型

        返回:
        - dict: 定时任务详情字典
        """
        exist_obj = await JobCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg="更新失败，该定时任务不存在")
        if (
            data.trigger == "cron"
            and data.trigger_args
            and not CronUtil.validate_cron_expression(data.trigger_args)
        ):
            raise CustomException(msg=f"新增定时任务{data.name}失败, Cron表达式不正确")
        obj = await JobCRUD(auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败，该数据定时任务不存在")
        SchedulerUtil().modify_job(job_id=obj.id)
        return JobOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_job_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除定时任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 定时任务ID列表
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            exist_obj = await JobCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg="删除失败，该数据定时任务不存在")
            obj = await JobLogCRUD(auth).get(job_id=id)
            if obj:
                raise CustomException(msg=f"删除失败，该定时任务存 {exist_obj.name} 在日志记录")

            SchedulerUtil().remove_job(job_id=id)
        await JobCRUD(auth).delete_obj_crud(ids=ids)

    @classmethod
    async def clear_job_service(cls, auth: AuthSchema) -> None:
        """
        清空所有定时任务

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        SchedulerUtil().clear_jobs()
        await JobLogCRUD(auth).clear_obj_log_crud()
        await JobCRUD(auth).clear_obj_crud()

    @classmethod
    async def option_job_service(cls, auth: AuthSchema, id: int, option: int) -> None:
        """
        操作定时任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 定时任务ID
        - option (int): 操作类型, 1: 暂停 2: 恢复 3: 重启
        """
        # 1: 暂停 2: 恢复 3: 重启
        obj = await JobCRUD(auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="操作失败，该数据定时任务不存在")
        if option == 1:
            SchedulerUtil().pause_job(job_id=id)
            await JobCRUD(auth).set_obj_field_crud(ids=[id], status="1")  # 更新为暂停状态(1)
        elif option == 2:
            SchedulerUtil().resume_job(job_id=id)
            await JobCRUD(auth).set_obj_field_crud(ids=[id], status="0")  # 更新为运行状态(0)
        elif option == 3:
            # 重启任务：先移除再添加，确保使用最新的任务配置
            SchedulerUtil().remove_job(job_id=id)
            # 获取最新的任务配置
            updated_job = await JobCRUD(auth).get_obj_by_id_crud(id=id)
            if updated_job:
                # 重新添加任务
                SchedulerUtil().add_job(job_info=updated_job)
                # 设置状态为运行中
                await JobCRUD(auth).set_obj_field_crud(ids=[id], status="0")

    @classmethod
    async def export_job_service(cls, data_list: list[dict]) -> bytes:
        """
        导出定时任务列表

        参数:
        - data_list (list[dict]): 定时任务列表

        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            "id": "编号",
            "name": "任务名称",
            "func": "任务函数",
            "trigger": "触发器",
            "args": "位置参数",
            "kwargs": "关键字参数",
            "coalesce": "是否合并运行",
            "max_instances": "最大实例数",
            "jobstore": "任务存储",
            "executor": "任务执行器",
            "trigger_args": "触发器参数",
            "status": "任务状态",
            "message": "日志信息",
            "description": "备注",
            "created_time": "创建时间",
            "updated_time": "更新时间",
            "created_id": "创建者ID",
            "updated_id": "更新者ID",
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            item["status"] = (
                "运行中"
                if item["status"] == "0"
                else "暂停中"
                if item["status"] == "1"
                else "未知状态"
            )

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)


class JobLogService:
    """
    定时任务日志管理模块服务层
    """

    @classmethod
    async def get_job_log_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取定时任务日志详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 定时任务日志ID

        返回:
        - dict: 定时任务日志详情字典
        """
        obj = await JobLogCRUD(auth).get_obj_log_by_id_crud(id=id)
        return JobLogOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_job_log_list_service(
        cls,
        auth: AuthSchema,
        search: JobLogQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[dict]:
        """
        获取定时任务日志列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (JobLogQueryParam | None): 查询参数模型, 包含分页信息和查询条件
        - order_by (list[dict] | None): 排序参数列表, 每个元素为一个字典, 包含字段名和排序方向

        返回:
        - list[dict]: 定时任务日志详情字典列表
        """
        obj_list = await JobLogCRUD(auth).get_obj_log_list_crud(
            search=search.__dict__, order_by=order_by
        )
        return [JobLogOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def delete_job_log_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除定时任务日志

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 定时任务日志ID列表
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            exist_obj = await JobLogCRUD(auth).get_obj_log_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg=f"删除失败，该定时任务日志ID为{id}的记录不存在")
        await JobLogCRUD(auth).delete_obj_log_crud(ids=ids)

    @classmethod
    async def clear_job_log_service(cls, auth: AuthSchema) -> None:
        """
        清空定时任务日志

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        # 获取所有日志ID并批量删除
        all_logs = await JobLogCRUD(auth).get_obj_log_list_crud()
        if all_logs:
            ids = [log.id for log in all_logs]
            await JobLogCRUD(auth).delete_obj_log_crud(ids=ids)

    @classmethod
    async def export_job_log_service(cls, data_list: list[dict]) -> bytes:
        """
        导出定时任务日志列表

        参数:
        - data_list (List[Dict[str, Any]]): 定时任务日志列表

        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            "id": "编号",
            "job_name": "任务名称",
            "job_group": "任务组名",
            "job_executor": "任务执行器",
            "invoke_target": "调用目标字符串",
            "job_args": "位置参数",
            "job_kwargs": "关键字参数",
            "job_trigger": "任务触发器",
            "job_message": "日志信息",
            "exception_info": "异常信息",
            "status": "执行状态",
            "created_time": "创建时间",
            "updated_time": "更新时间",
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            item["status"] = "成功" if item.get("status") == "0" else "失败"

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
