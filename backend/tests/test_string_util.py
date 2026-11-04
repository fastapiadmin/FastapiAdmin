"""StringUtil 全分支测试。"""

from app.utils.string_util import StringUtil


def test_blank_and_empty() -> None:
    assert StringUtil.is_blank("") is True
    assert StringUtil.is_blank("   ") is True
    assert StringUtil.is_blank(" a ") is False
    assert StringUtil.is_empty(None) is True
    assert StringUtil.is_empty("") is True
    assert StringUtil.is_empty("x") is False
    assert StringUtil.is_not_empty("x") is True
    assert StringUtil.is_not_empty(None) is False


def test_http_and_case_helpers() -> None:
    assert StringUtil.is_http("http://x") is True
    assert StringUtil.is_http("https://x") is True
    assert StringUtil.is_http("ftp://x") is False
    assert StringUtil.contains_ignore_case("Hello World", "WORLD") is True
    assert StringUtil.contains_ignore_case("", "x") is False
    assert StringUtil.contains_any_ignore_case("Hello", ["x", "HEL"]) is True
    assert StringUtil.contains_any_ignore_case("", ["x"]) is False
    assert StringUtil.equals_ignore_case("ABC", "abc") is True
    assert StringUtil.equals_ignore_case("", "abc") is False
    assert StringUtil.equals_any_ignore_case("ABC", ["x", "abc"]) is True
    assert StringUtil.equals_any_ignore_case("", ["abc"]) is False
    assert StringUtil.startswith_case("Hello", "He") is True
    assert StringUtil.startswith_case("", "He") is False
    assert StringUtil.startswith_any_case("Hello", ["x", "He"]) is True
    assert StringUtil.startswith_any_case("", ["He"]) is False


def test_camel_case_conversions() -> None:
    assert StringUtil.convert_to_camel_case("") == ""
    assert StringUtil.convert_to_camel_case("user") == "User"
    assert StringUtil.convert_to_camel_case("user_name") == "UserName"
    assert StringUtil.convert_to_camel_case("user__name") == "UserName"
    assert StringUtil.to_lower_camel_case("") == ""
    assert StringUtil.to_lower_camel_case("user") == "user"
    assert StringUtil.to_lower_camel_case("user_name") == "userName"
    assert StringUtil.to_lower_camel_case("user__name") == "userName"


def test_mapping_lookup_ignore_case() -> None:
    mapping = {"Name": "n", "ROLE": "r"}
    assert StringUtil.get_mapping_value_by_key_ignore_case(mapping, "name") == "n"
    assert StringUtil.get_mapping_value_by_key_ignore_case(mapping, "role") == "r"
    assert StringUtil.get_mapping_value_by_key_ignore_case(mapping, "missing") == ""
