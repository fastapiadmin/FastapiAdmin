"""
合规诊断评分服务 v1.0

根据主办机构性质进行合规性评估和评分
"""
from dataclasses import dataclass
from typing import Any

from app.core.logger import log

from ..info_collection.model import ConsultationInfoModel, OrganizerNature
from .model import ComplianceDiagnosisModel


@dataclass
class ComplianceScoreResult:
    """合规评分结果"""
    score: int                          # 合规评分(0-100)
    level: str                          # 合规等级(low/medium/high)
    is_high_risk: bool                  # 是否高风险
    risk_factors: list[str]             # 风险因素列表
    improvement_suggestions: list[str]  # 改进建议列表
    diagnosis_details: dict[str, Any]   # 诊断详情


class ComplianceScoringServiceV1:
    """
    合规诊断评分服务 v1.0

    评分规则：
    主办机构性质 	 |  得分
    单一省、市、区级官方机构（电视台、电台、考试院、教育局） 	 |  	 8-10
    单一高中、高校 	 |  5-8
    单一第三方机构 	 |  	 0-3
    多所高中联合、无第三方机构 	 |  	 8-10
    多所高中联合、有第三方机构 	 |  	 6-9
    多家第三方机构 	 |  	 3-6
    """

    # 主办机构性质评分规则
    ORGANIZER_NATURE_SCORES = {
        OrganizerNature.OFFICIAL_SINGLE: {
            "min_score": 8,
            "max_score": 10,
            "base_score": 9,
            "risk_level": "low",
            "description": "单一省、市、区级官方机构",
        },
        OrganizerNature.HIGH_SCHOOL_SINGLE: {
            "min_score": 5,
            "max_score": 8,
            "base_score": 6.5,
            "risk_level": "medium",
            "description": "单一高中",
        },
        OrganizerNature.UNIVERSITY_SINGLE: {
            "min_score": 5,
            "max_score": 8,
            "base_score": 6.5,
            "risk_level": "medium",
            "description": "单一高校",
        },
        OrganizerNature.THIRD_PARTY_SINGLE: {
            "min_score": 0,
            "max_score": 3,
            "base_score": 1.5,
            "risk_level": "high",
            "description": "单一第三方机构",
        },
        OrganizerNature.HIGH_SCHOOL_UNION: {
            "min_score": 8,
            "max_score": 10,
            "base_score": 9,
            "risk_level": "low",
            "description": "多所高中联合、无第三方机构",
        },
        OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD: {
            "min_score": 6,
            "max_score": 9,
            "base_score": 7.5,
            "risk_level": "medium",
            "description": "多所高中联合、有第三方机构",
        },
        OrganizerNature.THIRD_PARTY_MULTIPLE: {
            "min_score": 3,
            "max_score": 6,
            "base_score": 4.5,
            "risk_level": "high",
            "description": "多家第三方机构",
        },
    }

    @classmethod
    async def diagnose_consultation(cls, consultation: ConsultationInfoModel) -> ComplianceScoreResult:
        """
        对咨询会进行合规诊断评分

        参数:
        - consultation (ConsultationInfoModel): 咨询会信息模型

        返回:
        - ComplianceScoreResult: 合规评分结果
        """
        log.info(f"开始对咨询会进行合规诊断: {consultation.title}")

        # 获取主办机构性质
        organizer_nature = cls._get_organizer_nature(consultation)

        # 计算基础评分
        base_score = cls._calculate_base_score(organizer_nature)

        # 评估风险因素
        risk_factors = cls._evaluate_risk_factors(consultation, organizer_nature)

        # 计算最终评分
        final_score = cls._calculate_final_score(base_score, risk_factors)

        # 确定合规等级
        compliance_level = cls._determine_compliance_level(final_score)

        # 判断是否高风险
        is_high_risk = cls._is_high_risk(organizer_nature, final_score)

        # 生成改进建议
        improvement_suggestions = cls._generate_improvement_suggestions(
            organizer_nature, risk_factors
        )

        # 构建诊断详情
        diagnosis_details = cls._build_diagnosis_details(
            consultation, organizer_nature, base_score, final_score, risk_factors
        )

        result = ComplianceScoreResult(
            score=final_score,
            level=compliance_level,
            is_high_risk=is_high_risk,
            risk_factors=risk_factors,
            improvement_suggestions=improvement_suggestions,
            diagnosis_details=diagnosis_details,
        )

        log.info(f"合规诊断完成: 评分={final_score}, 等级={compliance_level}, 高风险={is_high_risk}")
        return result

    @classmethod
    def _get_organizer_nature(cls, consultation: ConsultationInfoModel) -> OrganizerNature:
        """获取主办机构性质"""
        if consultation.organizer_nature:
            try:
                return OrganizerNature(consultation.organizer_nature)
            except ValueError:
                pass

        # 根据主办方信息推断
        return cls._infer_organizer_nature(consultation)

    @classmethod
    def _infer_organizer_nature(cls, consultation: ConsultationInfoModel) -> OrganizerNature:
        """根据主办方信息推断机构性质"""
        organizer = consultation.organizer
        has_third_party = consultation.has_third_party

        # 判断是否为官方机构
        official_keywords = ["教育", "考试", "招生", "电视台", "电台", "政府"]
        if any(keyword in organizer for keyword in official_keywords):
            return OrganizerNature.OFFICIAL_SINGLE

        # 判断是否为高中
        high_school_keywords = ["中学", "高中", "一中", "二中", "附中"]
        if any(keyword in organizer for keyword in high_school_keywords):
            if "联合" in organizer or "、" in organizer:
                if has_third_party:
                    return OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD
                return OrganizerNature.HIGH_SCHOOL_UNION
            return OrganizerNature.HIGH_SCHOOL_SINGLE

        # 判断是否为高校
        university_keywords = ["大学", "学院"]
        if any(keyword in organizer for keyword in university_keywords):
            return OrganizerNature.UNIVERSITY_SINGLE

        # 判断是否为多家第三方机构
        if "、" in organizer or "联合" in organizer or "多家" in organizer:
            return OrganizerNature.THIRD_PARTY_MULTIPLE

        # 默认为单一第三方机构
        return OrganizerNature.THIRD_PARTY_SINGLE

    @classmethod
    def _calculate_base_score(cls, organizer_nature: OrganizerNature) -> float:
        """计算基础评分"""
        rule = cls.ORGANIZER_NATURE_SCORES.get(organizer_nature)
        if not rule:
            return 5.0  # 默认评分

        return rule["base_score"]

    @classmethod
    def _evaluate_risk_factors(
        cls, consultation: ConsultationInfoModel, organizer_nature: OrganizerNature
    ) -> list[str]:
        """评估风险因素"""
        risk_factors = []

        # 检查主办方性质风险
        if organizer_nature in [
            OrganizerNature.THIRD_PARTY_SINGLE,
            OrganizerNature.THIRD_PARTY_MULTIPLE,
        ]:
            risk_factors.append("主办方为商业机构，存在盈利性质风险")

        # 检查第三方参与风险
        if consultation.has_third_party:
            risk_factors.append("有第三方机构参与，需关注合作规范性")

        # 检查费用风险
        if consultation.booth_fee and consultation.booth_fee > 2000:
            risk_factors.append(f"展位费用较高({consultation.booth_fee}元)，需关注收费合理性")

        # 检查规模风险
        if consultation.estimated_visitors and consultation.estimated_visitors > 5000:
            risk_factors.append("预计参与人数较多，需关注现场管理能力")

        # 检查高校数量风险
        if consultation.university_count < 5:
            risk_factors.append("参与高校数量较少，咨询会价值可能有限")

        return risk_factors

    @classmethod
    def _calculate_final_score(cls, base_score: float, risk_factors: list[str]) -> int:
        """计算最终评分"""
        # 每个风险因素扣1分
        deduction = len(risk_factors) * 1.0

        final_score = base_score * 10 - deduction  # 转换为百分制
        final_score = max(0, min(100, int(final_score)))  # 限制在0-100之间

        return final_score

    @classmethod
    def _determine_compliance_level(cls, score: int) -> str:
        """确定合规等级"""
        if score >= 80:
            return "high"
        elif score >= 60:
            return "medium"
        else:
            return "low"

    @classmethod
    def _is_high_risk(cls, organizer_nature: OrganizerNature, score: int) -> bool:
        """判断是否高风险"""
        # 第三方机构且评分低于60分
        if organizer_nature in [
            OrganizerNature.THIRD_PARTY_SINGLE,
            OrganizerNature.THIRD_PARTY_MULTIPLE,
        ] and score < 60:
            return True

        # 评分低于40分
        if score < 40:
            return True

        return False

    @classmethod
    def _generate_improvement_suggestions(
        cls, organizer_nature: OrganizerNature, risk_factors: list[str]
    ) -> list[str]:
        """生成改进建议"""
        suggestions = []

        # 根据机构性质给出建议
        if organizer_nature == OrganizerNature.THIRD_PARTY_SINGLE:
            suggestions.append("建议引入教育部门或学校作为联合主办方，提升活动公信力")
            suggestions.append("建议公开活动收支明细，增强透明度")
        elif organizer_nature == OrganizerNature.THIRD_PARTY_MULTIPLE:
            suggestions.append("建议明确各主办方的权责分工")
            suggestions.append("建议建立联合审核机制，确保活动内容合规")
        elif organizer_nature == OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD:
            suggestions.append("建议学校方加强对第三方机构的监督")
            suggestions.append("建议明确第三方机构的参与范围和权限")

        # 根据风险因素给出建议
        if "展位费用较高" in str(risk_factors):
            suggestions.append("建议合理控制展位费用，避免给高校造成过重负担")

        if "参与人数较多" in str(risk_factors):
            suggestions.append("建议制定详细的安全预案，确保现场秩序")

        if "参与高校数量较少" in str(risk_factors):
            suggestions.append("建议扩大邀请范围，吸引更多高校参与")

        return suggestions

    @classmethod
    def _build_diagnosis_details(
        cls,
        consultation: ConsultationInfoModel,
        organizer_nature: OrganizerNature,
        base_score: float,
        final_score: int,
        risk_factors: list[str],
    ) -> dict[str, Any]:
        """构建诊断详情"""
        rule = cls.ORGANIZER_NATURE_SCORES.get(organizer_nature, {})

        return {
            "consultation_id": consultation.id,
            "consultation_title": consultation.title,
            "organizer": consultation.organizer,
            "organizer_nature": organizer_nature.value,
            "organizer_nature_description": rule.get("description", "未知"),
            "scoring_rule_version": "1.0",
            "scoring_breakdown": {
                "base_score": base_score,
                "base_score_max": rule.get("max_score", 10),
                "risk_factor_count": len(risk_factors),
                "risk_factor_deduction": len(risk_factors) * 1.0,
                "final_score": final_score,
            },
            "risk_assessment": {
                "risk_level": rule.get("risk_level", "medium"),
                "risk_factors": risk_factors,
            },
        }

    @classmethod
    async def save_diagnosis_result(
        cls,
        consultation_id: int,
        result: ComplianceScoreResult,
    ) -> ComplianceDiagnosisModel:
        """
        保存诊断结果

        参数:
        - consultation_id (int): 咨询会ID
        - result (ComplianceScoreResult): 诊断结果

        返回:
        - ComplianceDiagnosisModel: 保存的诊断记录
        """
        from datetime import datetime

        # 将之前的诊断记录标记为非最新
        await cls._mark_previous_as_not_latest(consultation_id)

        # 创建新的诊断记录
        diagnosis = ComplianceDiagnosisModel(
            consultation_id=consultation_id,
            diagnosis_time=datetime.now(),
            compliance_score=result.score,
            compliance_level=result.level,
            risk_factors=result.risk_factors,
            diagnosis_details=result.diagnosis_details,
            improvement_suggestions=result.improvement_suggestions,
            is_high_risk=result.is_high_risk,
            risk_warning=";".join(result.risk_factors) if result.risk_factors else None,
            is_latest=True,
        )

        # 更新咨询会的合规评分
        await cls._update_consultation_compliance_score(consultation_id, result)

        return diagnosis

    @classmethod
    async def _mark_previous_as_not_latest(cls, consultation_id: int) -> None:
        """将之前的诊断记录标记为非最新"""
        from sqlalchemy import update

        from app.core.database import async_session

        async with async_session() as session:
            await session.execute(
                update(ComplianceDiagnosisModel)
                .where(ComplianceDiagnosisModel.consultation_id == consultation_id)
                .values(is_latest=False)
            )
            await session.commit()

    @classmethod
    async def _update_consultation_compliance_score(
        cls, consultation_id: int, result: ComplianceScoreResult
    ) -> None:
        """更新咨询会的合规评分"""
        from sqlalchemy import update

        from app.core.database import async_session

        async with async_session() as session:
            await session.execute(
                update(ConsultationInfoModel)
                .where(ConsultationInfoModel.id == consultation_id)
                .values(
                    compliance_score=result.score,
                    compliance_level=result.level,
                )
            )
            await session.commit()

    @classmethod
    async def batch_diagnose_consultations(cls, consultation_ids: list[int]) -> dict[int, ComplianceScoreResult]:
        """
        批量诊断咨询会

        参数:
        - consultation_ids (list[int]): 咨询会ID列表

        返回:
        - dict[int, ComplianceScoreResult]: 诊断结果字典
        """
        from app.core.database import async_session

        results = {}
        async with async_session() as session:
            for consultation_id in consultation_ids:
                try:
                    # 获取咨询会信息
                    consultation = await session.get(ConsultationInfoModel, consultation_id)
                    if not consultation:
                        log.warning(f"咨询会不存在: {consultation_id}")
                        continue

                    # 进行诊断
                    result = await cls.diagnose_consultation(consultation)

                    # 保存结果
                    await cls.save_diagnosis_result(consultation_id, result)

                    results[consultation_id] = result

                except Exception as e:
                    log.error(f"诊断咨询会失败 {consultation_id}: {e}")
                    continue

        return results
