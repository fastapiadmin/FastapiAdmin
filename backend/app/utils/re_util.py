import re


def search_string(pattern: str, text: str) -> re.Match[str] | None:
    """
    全字段正则匹配

    参数:
    - pattern (str): 正则表达式模式。
    - text (str): 待匹配的文本。

    返回:
    - re.Match[str] | None: 匹配结果。
    """
    if not pattern or not text:
        return None

    result = re.search(pattern, text)
    return result


def match_string(pattern: str, text: str) -> re.Match[str] | None:
    """
    从字段开头正则匹配

    参数:
    - pattern (str): 正则表达式模式。
    - text (str): 待匹配的文本。

    返回:
    - re.Match[str] | None: 匹配结果。
    """
    if not pattern or not text:
        return None

    result = re.match(pattern, text)
    return result


def is_phone(number: str) -> re.Match[str] | None:
    """
    检查手机号码格式

    参数:
    - number (str): 待检查的手机号码。

    返回:
    - re.Match[str] | None: 匹配结果。
    """
    if not number:
        return None

    phone_pattern = r"^1[3-9]\d{9}$"
    return match_string(phone_pattern, number)


def is_git_url(url: str) -> re.Match[str] | None:
    """
    检查 git URL 格式

    参数:
    - url (str): 待检查的 URL。

    返回:
    - re.Match[str] | None: 匹配结果。
    """
    if not url:
        return None

    git_pattern = r"^(?!(git\+ssh|ssh)://|git@)(?P<scheme>git|https?|file)://(?P<host>[^/]*)(?P<path>(?:/[^/]*)*/)(?P<repo>[^/]+?)(?:\.git)?$"
    return match_string(git_pattern, url)
