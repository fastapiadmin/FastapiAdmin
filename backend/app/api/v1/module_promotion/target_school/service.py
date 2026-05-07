"""
目标学校管理 - 服务层
"""

import io

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.excel_util import ExcelUtil

from .crud import TargetSchoolCRUD
from .model import FollowStatus, IntentionLevel
from .schema import (
    TargetSchoolOutSchema,
    TargetSchoolQuerySchema,
)


class TargetSchoolService:
    """
    目标学校管理服务层

    职责：目标学校增删改查、跟进记录维护(拜访内容/次数/下次计划)、按组/按负责人查询
    约束：学校代码(school_code)唯一
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 目标学校ID

        返回:
        - dict: 目标学校模型实例字典
        """
        obj = await TargetSchoolCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该目标学校不存在")
        return TargetSchoolOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: TargetSchoolQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (TargetSchoolQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 目标学校模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await TargetSchoolCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [TargetSchoolOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: TargetSchoolQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (TargetSchoolQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await TargetSchoolCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建目标学校

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的目标学校模型实例字典
        """
        if data.get("school_code"):
            existing = await TargetSchoolCRUD(auth).get_by_school_code_crud(data["school_code"])
            if existing:
                raise CustomException(msg="学校代码已存在")

        obj = await TargetSchoolCRUD(auth).create_crud(data=data)
        log.info(f"创建目标学校成功: {obj.id}")
        return TargetSchoolOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新目标学校

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 目标学校ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的目标学校模型实例字典
        """
        existing = await TargetSchoolCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该目标学校不存在")

        if data.get("school_code") and data["school_code"] != existing.school_code:
            code_existing = await TargetSchoolCRUD(auth).get_by_school_code_crud(
                data["school_code"]
            )
            if code_existing:
                raise CustomException(msg="学校代码已存在")

        obj = await TargetSchoolCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新目标学校成功: {id}")
        return TargetSchoolOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除目标学校

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 目标学校ID
        """
        existing = await TargetSchoolCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该目标学校不存在")

        await TargetSchoolCRUD(auth).delete_crud(id=id)
        log.info(f"删除目标学校成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除目标学校

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 目标学校ID列表
        """
        await TargetSchoolCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除目标学校成功: {ids}")

    @classmethod
    async def follow_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        跟进目标学校

        支持更新的字段：visit_content(拜访内容) -> 自动累加拜访次数
        visit_date / next_visit_plan / next_visit_date / follow_status
        """
        existing = await TargetSchoolCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该目标学校不存在")

        update_data = {}

        # 提交拜访内容时自动累加拜访次数
        if "visit_content" in data:
            update_data["last_visit_content"] = data["visit_content"]
            update_data["visit_count"] = existing.visit_count + 1

        if "visit_date" in data:
            update_data["last_visit_date"] = data["visit_date"]

        if "next_visit_plan" in data:
            update_data["next_visit_plan"] = data["next_visit_plan"]

        if "next_visit_date" in data:
            update_data["next_visit_date"] = data["next_visit_date"]

        if "follow_status" in data:
            update_data["follow_status"] = data["follow_status"]

        obj = await TargetSchoolCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"跟进目标学校成功: {id}")
        return TargetSchoolOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_by_team_service(cls, auth: AuthSchema, team_id: int) -> list[dict]:
        """
        获取招生组下所有目标学校

        参数:
        - auth (AuthSchema): 认证信息模型
        - team_id (int): 招生组ID

        返回:
        - list[dict]: 目标学校列表
        """
        obj_list = await TargetSchoolCRUD(auth).get_by_team_id_crud(team_id=team_id)
        return [TargetSchoolOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def get_by_personnel_service(cls, auth: AuthSchema, personnel_id: int) -> list[dict]:
        """
        获取负责人下所有目标学校

        参数:
        - auth (AuthSchema): 认证信息模型
        - personnel_id (int): 负责人ID

        返回:
        - list[dict]: 目标学校列表
        """
        obj_list = await TargetSchoolCRUD(auth).get_by_personnel_id_crud(personnel_id=personnel_id)
        return [TargetSchoolOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def batch_import_service(
        cls, auth: AuthSchema, file: UploadFile, update_support: bool = False
    ) -> str:
        """
        批量导入目标学校

        去重规则：name（学校名称）
        """
        header_dict = {
            "学校名称": "name",
            "学校类型": "school_type",
            "省份": "province",
            "城市": "city",
            "联系人": "contact_person",
            "联系电话": "contact_phone",
            "学生规模": "student_scale",
            "意向级别": "intention_level",
        }

        # 中文意向级别 -> 枚举值
        intention_level_map = {
            "高意向": IntentionLevel.HIGH.value,
            "中意向": IntentionLevel.MEDIUM.value,
            "低意向": IntentionLevel.LOW.value,
        }

        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()

            if df.empty:
                raise CustomException(msg="导入文件为空")

            missing_headers = [h for h in header_dict.keys() if h not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")

            df.rename(columns=header_dict, inplace=True)

            required_fields = ["name"]
            errors = []
            for field in required_fields:
                missing_rows = df[df[field].isnull()].index.tolist()
                if missing_rows:
                    field_name = next(k for k, v in header_dict.items() if v == field)
                    rows_str = "、".join([str(i + 1) for i in missing_rows])
                    errors.append(f"{field_name}不能为空，第{rows_str}行")

            if errors:
                raise CustomException(msg="；".join(errors))

            error_msgs = []
            success_count = 0
            count = 0

            for _index, row in df.iterrows():
                try:
                    count += 1

                    name = str(row["name"]).strip() if pd.notna(row["name"]) else None
                    if not name:
                        error_msgs.append(f"第{count}行: 学校名称不能为空")
                        continue

                    school_type = (
                        str(row["school_type"]).strip() if pd.notna(row["school_type"]) else None
                    )
                    province = str(row["province"]).strip() if pd.notna(row["province"]) else None
                    city = str(row["city"]).strip() if pd.notna(row["city"]) else None
                    contact_person = (
                        str(row["contact_person"]).strip()
                        if pd.notna(row["contact_person"])
                        else None
                    )
                    contact_phone = (
                        str(row["contact_phone"]).strip()
                        if pd.notna(row["contact_phone"])
                        else None
                    )
                    student_scale = (
                        int(row["student_scale"]) if pd.notna(row["student_scale"]) else None
                    )
                    # 意向级别中文映射
                    intention_raw = (
                        str(row["intention_level"]).strip()
                        if pd.notna(row["intention_level"])
                        else None
                    )
                    intention_level = intention_level_map.get(intention_raw, intention_raw)

                    school_data = {
                        "name": name,
                        "school_type": school_type,
                        "province": province,
                        "city": city,
                        "contact_person": contact_person,
                        "contact_phone": contact_phone,
                        "student_scale": student_scale,
                        "intention_level": intention_level,
                        "follow_status": FollowStatus.NEW.value,
                    }

                    # 按学校名称去重
                    existing_list = await TargetSchoolCRUD(auth).list_crud(
                        search={"name": ("eq", name)}
                    )
                    if existing_list:
                        if update_support:
                            await TargetSchoolCRUD(auth).update_crud(
                                id=existing_list[0].id, data=school_data
                            )
                            success_count += 1
                        else:
                            error_msgs.append(f"第{count}行: 学校 {name} 已存在")
                        continue

                    await TargetSchoolCRUD(auth).create_crud(data=school_data)
                    success_count += 1

                except Exception as e:
                    error_msgs.append(f"第{count}行: 异常{e!s}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result

        except CustomException:
            raise
        except Exception as e:
            log.error(f"批量导入目标学校失败: {e!s}")
            raise CustomException(msg=f"导入失败: {e!s}")

    @classmethod
    async def import_template_download_service(cls) -> bytes:
        """获取目标学校导入模板"""
        header_list = [
            "学校名称",
            "学校类型",
            "省份",
            "城市",
            "联系人",
            "联系电话",
            "学生规模",
            "意向级别",
        ]
        selector_header_list = ["学校类型", "意向级别"]
        option_list = [
            {"学校类型": ["重点高中", "普通高中", "职业高中", "完全中学"]},
            {"意向级别": ["高意向", "中意向", "低意向"]},
        ]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list,
        )
