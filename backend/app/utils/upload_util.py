import mimetypes
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import aiofiles
from fastapi import UploadFile

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log


class UploadUtil:
    """
    上传工具类
    """

    @staticmethod
    def generate_random_number() -> str:
        """
        生成3位随机数字字符串。

        返回:
        - str: 三位随机数字字符串。
        """
        return f"{random.randint(1, 999):03}"

    @staticmethod
    def check_file_exists(filepath: str) -> bool:
        """
        检查文件是否存在。

        参数:
        - filepath (str): 文件路径。

        返回:
        - bool: 文件是否存在。
        """
        return Path(filepath).exists()

    @staticmethod
    def check_file_extension(file: UploadFile) -> bool:
        """
        检查文件后缀是否合法。

        参数:
        - file (UploadFile): 上传的文件对象。

        返回:
        - bool: 文件后缀是否合法。

        异常:
        - CustomException: 文件类型不支持时抛出。
        """
        if file.content_type:
            file_extension = mimetypes.guess_extension(file.content_type)
            if file_extension and file_extension in settings.ALLOWED_EXTENSIONS:
                return True
            raise CustomException(msg="文件类型不支持")
        raise CustomException(msg="文件类型不支持")

    @staticmethod
    def check_file_timestamp(filename: str) -> bool:
        """
        校验文件时间戳是否合法。

        参数:
        - filename (str): 文件名（包含时间戳片段）。

        返回:
        - bool: 时间戳是否合法。
        """
        try:
            name_parts = filename.rsplit(".", 1)[0].split("_")
            timestamp = name_parts[-1].split(settings.UPLOAD_MACHINE)[0]
            datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            return True
        except (ValueError, IndexError):
            return False

    @staticmethod
    def check_file_machine(filename: str) -> bool:
        """
        校验文件机器码是否合法。

        参数:
        - filename (str): 文件名。

        返回:
        - bool: 机器码是否合法。
        """
        try:
            name_without_ext = filename.rsplit(".", 1)[0]
            return len(name_without_ext) >= 4 and name_without_ext[-4] == settings.UPLOAD_MACHINE
        except IndexError:
            return False

    @staticmethod
    def check_file_random_code(filename: str) -> bool:
        """
        校验文件随机码是否合法。

        参数:
        - filename (str): 文件名。

        返回:
        - bool: 随机码是否合法（000–999）。
        """
        try:
            code = filename.rsplit(".", 1)[0][-3:]
            return code.isdigit() and 1 <= int(code) <= 999
        except IndexError:
            return False

    @staticmethod
    def check_file_size(file: UploadFile) -> bool:
        """
        校验文件大小是否合法。

        参数:
        - file (UploadFile): 上传的文件对象。

        返回:
        - bool: 文件大小是否合法（未提供 size 返回 False）。
        """
        if file.size:
            return file.size <= settings.MAX_FILE_SIZE
        return False

    @classmethod
    def generate_file_name(cls, filename: str) -> str:
        """
        生成文件名称。

        参数:
        - filename (str): 原始文件名（包含拓展名）。

        返回:
        - str: 生成的文件名（包含时间戳、机器码、随机码）。
        """
        name, ext = filename.rsplit(".", 1)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{name}_{timestamp}{settings.UPLOAD_MACHINE}{cls.generate_random_number()}.{ext}"

    @staticmethod
    def generate_file(filepath: Path, chunk_size: int = 8192):
        """
        根据文件生成二进制数据迭代器。

        参数:
        - filepath (Path): 文件路径。
        - chunk_size (int): 分块大小，默认 8192 字节。

        返回:
        - Iterator[bytes]: 文件二进制数据分块迭代器。
        """
        with filepath.open("rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    @staticmethod
    def delete_file(filepath: Path) -> bool:
        """
        删除文件。

        参数:
        - filepath (Path): 文件路径。

        返回:
        - bool: 删除是否成功。
        """
        try:
            filepath.unlink(missing_ok=True)
            return True
        except OSError:
            return False

    @classmethod
    async def upload_file(cls, file: UploadFile, base_url: str) -> tuple[str, Path, str]:
        """
        文件上传。

        参数:
        - file (UploadFile): 上传的文件对象。
        - base_url (str): 基础 URL。

        返回:
        - tuple[str, Path, str]: (文件名, 文件路径, 文件 URL)。

        异常:
        - CustomException: 当文件类型不支持或大小超限时抛出。
        """
        # 文件校验
        if not all([
            cls.check_file_extension(file),
            cls.check_file_size(file),
        ]):
            raise CustomException(msg="文件类型或大小不合法")

        try:
            # 构建完整的目录路径
            dir_path = settings.UPLOAD_FILE_PATH.joinpath(datetime.now().strftime("%Y/%m/%d"))
            dir_path.mkdir(parents=True, exist_ok=True)

            filename = ""
            # 生成文件名并保存
            if file.filename:
                filename = cls.generate_file_name(file.filename)
            filepath = dir_path.joinpath(filename)
            file_url = urljoin(base_url, str(filepath))
            # filepath.mkdir(parents=True, exist_ok=True)

            # 分块写入文件
            chunk_size = 8 * 1024 * 1024  # 8MB chunks
            async with aiofiles.open(filepath, "wb") as f:
                while chunk := await file.read(chunk_size):
                    await f.write(chunk)

            # 返回相对路径
            return filename, filepath, file_url

        except Exception as e:
            log.error(f"文件上传失败: {e}")
            raise CustomException(msg=f"文件上传失败: {e}")

    @staticmethod
    def get_file_tree(file_path: str) -> list[dict]:
        """
        获取文件树结构。

        参数:
        - file_path (str): 文件路径。

        返回:
        - list[dict]: 文件树列表。
        """
        return [{"name": item.name, "is_dir": item.is_dir()} for item in Path(file_path).iterdir()]

    @classmethod
    async def download_file(cls, file_path: str) -> str:
        """
        下载文件，生成新的文件名。

        参数:
        - file_path (str): 文件路径。

        返回:
        - str: 文件下载信息。
        """
        filename = cls.generate_file(Path(file_path))
        return str(filename)
