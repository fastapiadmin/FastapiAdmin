"""通用文件上传/下载服务边界。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import CustomException
from app.modules.common.file import service as S


async def test_upload_service(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(S.UploadUtil, "upload_file", AsyncMock(return_value=("a.txt", "/tmp/a.txt", "http://x/a.txt")))
    out = await S.FileService.upload_service("http://x", SimpleNamespace(filename="a.txt"))
    assert out.file_name == "a.txt"


def test_download_guards(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    import asyncio
    monkeypatch.setattr(S.settings, "UPLOAD_FILE_PATH", tmp_path)
    async def run():
        with pytest.raises(CustomException):
            await S.FileService.download_service("")
        with pytest.raises(CustomException):
            await S.FileService.download_service("../x")
        with pytest.raises(CustomException):
            await S.FileService.download_service(str(tmp_path.parent / "x"))
        with pytest.raises(CustomException):
            await S.FileService.download_service(str(tmp_path / "missing.txt"))
        f = tmp_path / "a.txt"; f.write_text("x")
        out = await S.FileService.download_service(str(f))
        assert out.file_name == "a.txt"
    asyncio.run(run())
