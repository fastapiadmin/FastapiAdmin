"""应用 lifespan 启停分支（依赖全部 mock）。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app import lifespan


async def test_lifespan_start_stop() -> None:
    app = SimpleNamespace(state=SimpleNamespace(redis=object()))
    with patch("app.scripts.initialize.InitializeData.init_db", new=AsyncMock()), \
         patch("app.modules.ai.chat.crud.init_agno_tables", new=AsyncMock()), \
         patch("app.core.redis_crud.redis_connect", new=AsyncMock()), \
         patch("app.modules.system.params.service.ParamsService.init_cache", new=AsyncMock()), \
         patch("app.modules.system.dict.service.DictDataService.init_cache", new=AsyncMock()), \
         patch("app.core.ap_scheduler.SchedulerUtil.init_scheduler", new=AsyncMock()), \
         patch("app.core.ap_scheduler.SchedulerUtil.shutdown", new=AsyncMock()), \
         patch("app.core.ap_scheduler.SchedulerUtil.is_scheduler_ready", new=MagicMock(return_value=True)), \
         patch("app.core.database.async_engine") as eng, \
         patch("app.console_start", new=MagicMock()) as cs, \
         patch("app.console_end", new=MagicMock()) as ce:
        eng.dispose = AsyncMock()
        async with lifespan(app):
            pass
    assert cs.called and ce.called and eng.dispose.await_count == 1
