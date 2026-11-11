"""调度任务 schema / 分页工具边缘。"""

from __future__ import annotations

import pytest

from app.core.base_schema import PageResultSchema


def test_job_schema() -> None:
    from app.modules.task.cronjob.job.schema import JobCreateSchema, SchedulerJobModifySchema
    assert SchedulerJobModifySchema(name="n").to_changes() == {"name": "n"}
    with pytest.raises(Exception):
        JobCreateSchema(job_id="")
    with pytest.raises(Exception):
        JobCreateSchema(job_id="x" * 65)
    with pytest.raises(Exception):
        JobCreateSchema(job_id="1", trigger_type="bad")
    assert JobCreateSchema(job_id=" 1 ", trigger_type="cron").job_id == "1"
    assert JobCreateSchema(job_id="1", trigger_type=None) is not None


async def test_pagination_util() -> None:
    from app.common.request import PaginationService
    p = await PaginationService.paginate([1, 2, 3], None, None)
    assert p.page_no == 1 and p.page_size == 10 and p.has_next is False
    p2 = await PaginationService.paginate([1, 2, 3], 1, 2)
    assert p2.items == [1, 2] and p2.has_next is True
    with pytest.raises(Exception):
        await PaginationService.paginate([1], 0, 10)
    with pytest.raises(Exception):
        await PaginationService.paginate([1], 1, 0)
