import bleach

ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "br",
    "code",
    "col",
    "colgroup",
    "dd",
    "del",
    "dl",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "span",
    "strike",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "tt",
    "u",
    "ul",
    "video",
    "source",
    "div",
    "font",
]

ALLOWED_ATTRIBUTES = {
    "*": ["class", "style", "id", "data-*"],
    "a": ["href", "title", "target", "rel"],
    "abbr": ["title"],
    "acronym": ["title"],
    "img": ["src", "alt", "title", "width", "height"],
    "video": ["src", "controls", "width", "height", "poster"],
    "source": ["src", "type"],
    "font": ["color", "size", "face"],
    "td": ["width", "height", "colspan", "rowspan"],
    "th": ["width", "height", "colspan", "rowspan"],
    "col": ["width", "span"],
    "colgroup": ["span"],
}

ALLOWED_STYLES = [
    "color",
    "background-color",
    "font-size",
    "font-family",
    "font-weight",
    "font-style",
    "text-decoration",
    "text-align",
    "margin",
    "margin-left",
    "margin-right",
    "margin-top",
    "margin-bottom",
    "padding",
    "padding-left",
    "padding-right",
    "padding-top",
    "padding-bottom",
    "border",
    "border-color",
    "border-width",
    "border-style",
    "width",
    "height",
    "line-height",
    "display",
]


def sanitize_html(content: str) -> str:
    """
    清理 HTML 内容，移除潜在的 XSS 攻击代码。

    参数:
    - content (str): 需要清理的 HTML 内容

    返回:
    - str: 清理后的安全 HTML 内容
    """
    if not content:
        return content

    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        strip_comments=True,
    )


def sanitize_html_with_styles(content: str) -> str:
    """
    清理 HTML 内容（包含样式），移除潜在的 XSS 攻击代码。

    参数:
    - content (str): 需要清理的 HTML 内容

    返回:
    - str: 清理后的安全 HTML 内容
    """
    if not content:
        return content

    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        strip_comments=True,
    )


def strip_all_tags(content: str) -> str:
    """
    移除所有 HTML 标签，只保留纯文本。

    参数:
    - content (str): 需要处理的 HTML 内容

    返回:
    - str: 纯文本内容
    """
    if not content:
        return content

    return bleach.clean(content, tags=[], attributes={}, strip=True)
