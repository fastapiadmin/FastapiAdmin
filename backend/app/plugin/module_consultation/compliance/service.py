"""
合规诊断 - 服务层
"""
from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ComplianceDiagnosisCRUD, ComplianceRuleCRUD
from .model import ComplianceDiagnosisModel
from .schema import (
    ComplianceCheckResultSchema,
    ComplianceDiagnosisCreateSchema,
    ComplianceDiagnosisOutSchema,
    ComplianceDiagnosisQuerySchema,
    ComplianceDiagnosisUpdateSchema,
    ComplianceRuleCreateSchema,
    ComplianceRuleOutSchema,
    ComplianceRuleQuerySchema,
    ComplianceRuleUpdateSchema,
)


class ComplianceDiagnosisService:
    """
    合规诊断服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await ComplianceDiagnosisCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该诊断记录不存在")
        return ComplianceDiagnosisOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ComplianceDiagnosisQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await ComplianceDiagnosisCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [ComplianceDiagnosisOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ComplianceDiagnosisQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ComplianceDiagnosisCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(
        cls, auth: AuthSchema, data: ComplianceDiagnosisCreateSchema
    ) -> dict:
        """创建诊断记录"""
        create_data = data.model_dump(exclude_unset=True)
        obj = await ComplianceDiagnosisCRUD(auth).create_crud(create_data)
        log.info(f"创建诊断记录成功 {obj.id}")
        return ComplianceDiagnosisOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: ComplianceDiagnosisUpdateSchema
    ) -> dict:
        """更新诊断记录"""
        obj = await ComplianceDiagnosisCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该诊断记录不存在")
        update_data = data.model_dump(exclude_unset=True)
        obj = await ComplianceDiagnosisCRUD(auth).update_crud(id, update_data)
        return ComplianceDiagnosisOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """删除"""
        obj = await ComplianceDiagnosisCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该诊断记录不存在")
        await ComplianceDiagnosisCRUD(auth).delete_crud(id)

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除"""
        await ComplianceDiagnosisCRUD(auth).batch_delete_crud(ids)

    @classmethod
    async def get_latest_by_consultation_service(
        cls, auth: AuthSchema, consultation_id: int
    ) -> dict | None:
        """获取某咨询会的最新诊断"""
        obj = await ComplianceDiagnosisCRUD(auth).get_latest_by_consultation_crud(consultation_id)
        if obj:
            return ComplianceDiagnosisOutSchema.model_validate(obj).model_dump()
        return None

    @classmethod
    async def check_compliance_service(
        cls, auth: AuthSchema, consultation_id: int
    ) -> dict:
        """执行合规检查"""
        from app.plugin.module_consultation.info_collection.crud import InfoCollectionCRUD

        consultation = await InfoCollectionCRUD(auth).get_by_id_crud(consultation_id)
        if not consultation:
            raise CustomException(msg="该咨询会不存在")

        active_rules = await ComplianceRuleCRUD(auth).get_active_rules_crud()

        passed_rules = []
        failed_rules = []
        risk_factors = []
        improvement_suggestions = []
        total_weight = 0
        deducted_score = 0

        for rule in active_rules:
            passed, reason = cls._check_rule(rule, consultation)
            if passed:
                passed_rules.append(rule.name)
            else:
                failed_rules.append(rule.name)
                risk_factors.append(f"{rule.name}: {reason}")
                improvement_suggestions.append(f"建议: {rule.description}")
                deducted_score += rule.rule_weight

        compliance_score = max(0, 100 - deducted_score)

        if compliance_score >= 80:
            compliance_level = "low"
        elif compliance_score >= 60:
            compliance_level = "medium"
        else:
            compliance_level = "high"

        is_high_risk = compliance_level == "high" or compliance_score < 60

        result_data = {
            "consultation_id": consultation_id,
            "compliance_score": compliance_score,
            "compliance_level": compliance_level,
            "risk_factors": risk_factors,
            "improvement_suggestions": improvement_suggestions,
            "is_high_risk": is_high_risk,
            "passed_rules": passed_rules,
            "failed_rules": failed_rules,
        }

        diagnosis_data = {
            "consultation_id": consultation_id,
            "compliance_score": compliance_score,
            "compliance_level": compliance_level,
            "risk_factors": risk_factors,
            "diagnosis_details": result_data,
            "improvement_suggestions": improvement_suggestions,
            "is_high_risk": is_high_risk,
        }

        await ComplianceDiagnosisCRUD(auth).create_crud(diagnosis_data)
        log.info(f"合规检查完成 {consultation_id}, 评分: {compliance_score}")

        return result_data

    @classmethod
    def _check_rule(cls, rule: Any, consultation: Any) -> tuple[bool, str]:
        """检查单条规则"""
        rule_type = rule.rule_type
        condition = rule.rule_condition

        if rule_type == "organizer":
            organizer = getattr(consultation, "organizer", None) or ""
            forbidden_words = condition.get("forbidden_words", [])
            for word in forbidden_words:
                if word in organizer:
                    return False, f"主办方包含敏感词: {word}"
            return True, ""

        elif rule_type == "fee":
            booth_fee = getattr(consultation, "booth_fee", 0) or 0
            max_fee = condition.get("max_fee", 100000)
            if booth_fee > max_fee:
                return False, f"展位费超过上限: {booth_fee} > {max_fee}"
            return True, ""

        elif rule_type == "scale":
            estimated = getattr(consultation, "estimated_visitors", 0) or 0
            min_scale = condition.get("min_scale", 0)
            max_scale = condition.get("max_scale", 1000000)
            if estimated < min_scale or estimated > max_scale:
                return False, f"规模不符合要求: {estimated}"
            return True, ""

        elif rule_type == "location":
            city = getattr(consultation, "city", None) or ""
            allowed_cities = condition.get("allowed_cities", [])
            if allowed_cities and city not in allowed_cities:
                return False, f"城市不在允许范围内: {city}"
            return True, ""

        return True, ""


class ComplianceRuleService:
    """
    合规规则服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await ComplianceRuleCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该规则不存在")
        return ComplianceRuleOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ComplianceRuleQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await ComplianceRuleCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [ComplianceRuleOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ComplianceRuleQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ComplianceRuleCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(
        cls, auth: AuthSchema, data: ComplianceRuleCreateSchema
    ) -> dict:
        """创建规则"""
        create_data = data.model_dump(exclude_unset=True)
        obj = await ComplianceRuleCRUD(auth).create_crud(create_data)
        return ComplianceRuleOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: ComplianceRuleUpdateSchema
    ) -> dict:
        """更新规则"""
        obj = await ComplianceRuleCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该规则不存在")
        update_data = data.model_dump(exclude_unset=True)
        obj = await ComplianceRuleCRUD(auth).update_crud(id, update_data)
        return ComplianceRuleOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """删除"""
        obj = await ComplianceRuleCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该规则不存在")
        await ComplianceRuleCRUD(auth).delete_crud(id)

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除"""
        await ComplianceRuleCRUD(auth).batch_delete_crud(ids)

    @classmethod
    async def toggle_status_service(cls, auth: AuthSchema, id: int) -> dict:
        """切换启用状态"""
        obj = await ComplianceRuleCRUD(auth).toggle_status_crud(id)
        if not obj:
            raise CustomException(msg="该规则不存在")
        log.info(f"切换规则启用状态 {id}")
        return ComplianceRuleOutSchema.model_validate(obj).model_dump()
