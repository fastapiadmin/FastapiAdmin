import os

from fastapi import UploadFile

from app.config.setting import settings
from app.core.base_schema import DownloadFileSchema, UploadResponseSchema
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.upload_util import UploadUtil


class FileService:
    """
    文件管理服务层
    """

    @classmethod
    async def upload_service(
        cls, base_url: str, file: UploadFile, upload_type: str = "local"
    ) -> dict:
        """
        上传文件。

        参数:
        - base_url (str): 基础访问 URL。
        - file (UploadFile): 上传文件对象。
        - upload_type (str): 上传类型，'local' 或 'oss'，默认 'local'。

        返回:
        - Dict: 上传响应字典。

        异常:
        - CustomException: 当未选择文件或上传类型错误时抛出。
        """
        if upload_type == "local":
            filename, filepath, file_url = await UploadUtil.upload_file(
                file=file, base_url=base_url
            )
        else:
            raise CustomException(msg="上传类型错误")

        return UploadResponseSchema(
            file_path=f"{filepath}",
            file_name=filename,
            origin_name=file.filename,
            file_url=f"{file_url}",
        ).model_dump()

    @staticmethod
    def _validate_download_path(file_path: str) -> str:
        """
        验证下载路径是否安全。

        参数:
        - file_path (str): 文件路径。

        返回:
        - str: 安全的绝对路径。

        异常:
        - CustomException: 当路径不安全时抛出。
        """
        if not file_path:
            raise CustomException(msg="请选择要下载的文件")

        dangerous_patterns = ["../", "..\\", "\0"]
        for pattern in dangerous_patterns:
            if pattern in file_path:
                log.error(f"检测到路径穿越攻击: {file_path}")
                raise CustomException(msg="非法的文件路径")

        upload_root = settings.UPLOAD_FILE_PATH.resolve()
        abs_path = os.path.normpath(os.path.abspath(file_path))

        if not abs_path.startswith(str(upload_root)):
            log.error(f"路径不在上传目录内: {file_path}")
            raise CustomException(msg="非法的文件路径")

        return abs_path

    @classmethod
    async def download_service(cls, file_path: str) -> DownloadFileSchema:
        """
        下载文件。

        参数:
        - file_path (str): 文件路径。

        返回:
        - DownloadFileSchema: 下载文件响应对象。

        异常:
        - CustomException: 当未选择文件或文件不存在时抛出。
        """
        safe_path = cls._validate_download_path(file_path)

        if not UploadUtil.check_file_exists(safe_path):
            raise CustomException(msg="文件不存在")

        file_name = UploadUtil.download_file(safe_path)

        return DownloadFileSchema(
            file_path=safe_path,
            file_name=str(file_name),
        )
