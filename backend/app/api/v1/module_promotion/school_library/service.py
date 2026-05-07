"""
全国高中学校库 - 服务层
"""

import io

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.excel_util import ExcelUtil

from .crud import SchoolLibraryCRUD
from .schema import SchoolLibraryOutSchema, SchoolLibraryQuerySchema


class SchoolLibraryService:
    """
    全国高中学校库服务层

    职责：学校库增删改查、批量导入
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await SchoolLibraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该学校不存在")
        return SchoolLibraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: SchoolLibraryQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await SchoolLibraryCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """创建学校"""
        obj = await SchoolLibraryCRUD(auth).create_crud(data=data)
        log.info(f"创建学校成功: {obj.id}")
        return SchoolLibraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """更新学校"""
        existing = await SchoolLibraryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该学校不存在")

        obj = await SchoolLibraryCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新学校成功: {id}")
        return SchoolLibraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """删除学校"""
        existing = await SchoolLibraryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该学校不存在")

        await SchoolLibraryCRUD(auth).delete_crud(id=id)
        log.info(f"删除学校成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除学校"""
        await SchoolLibraryCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除学校成功: {ids}")

    @classmethod
    async def batch_import_service(
        cls, auth: AuthSchema, file: UploadFile, update_support: bool = False
    ) -> str:
        """
        批量导入学校库

        去重规则：name（学校名称）
        """
        header_dict = {
            "学校名称": "name",
            "学校编码": "school_code",
            "学校类型": "school_type",
            "省份": "province",
            "城市": "city",
            "区县": "district",
            "地址": "address",
            "联系电话": "contact_phone",
            "学生规模": "student_scale",
            "是否重点校": "is_key_school",
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

                    school_data = {
                        "name": name,
                        "school_code": (
                            str(row["school_code"]).strip()
                            if pd.notna(row["school_code"])
                            else None
                        ),
                        "school_type": (
                            str(row["school_type"]).strip()
                            if pd.notna(row["school_type"])
                            else None
                        ),
                        "province": (
                            str(row["province"]).strip() if pd.notna(row["province"]) else None
                        ),
                        "city": str(row["city"]).strip() if pd.notna(row["city"]) else None,
                        "district": (
                            str(row["district"]).strip() if pd.notna(row["district"]) else None
                        ),
                        "address": (
                            str(row["address"]).strip() if pd.notna(row["address"]) else None
                        ),
                        "contact_phone": (
                            str(row["contact_phone"]).strip()
                            if pd.notna(row["contact_phone"])
                            else None
                        ),
                        "student_scale": (
                            int(row["student_scale"]) if pd.notna(row["student_scale"]) else None
                        ),
                        "is_key_school": (
                            str(row["is_key_school"]).strip()
                            if pd.notna(row["is_key_school"])
                            else None
                        ),
                    }

                    # 按学校名称去重
                    existing_list = await SchoolLibraryCRUD(auth).list_crud(
                        search={"name": ("eq", name)}
                    )
                    if existing_list:
                        if update_support:
                            await SchoolLibraryCRUD(auth).update_crud(
                                id=existing_list[0].id, data=school_data
                            )
                            success_count += 1
                        else:
                            error_msgs.append(f"第{count}行: 学校 {name} 已存在")
                        continue

                    await SchoolLibraryCRUD(auth).create_crud(data=school_data)
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
            log.error(f"批量导入学校库失败: {e!s}")
            raise CustomException(msg=f"导入失败: {e!s}")

    @classmethod
    async def import_template_download_service(cls) -> bytes:
        """获取学校库导入模板"""
        header_list = [
            "学校名称",
            "学校编码",
            "学校类型",
            "省份",
            "城市",
            "区县",
            "地址",
            "联系电话",
            "学生规模",
            "是否重点校",
        ]
        selector_header_list = ["学校类型", "是否重点校"]
        option_list = [
            {"学校类型": ["重点高中", "普通高中", "职业高中", "完全中学"]},
            {"是否重点校": ["是", "否"]},
        ]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list,
        )
