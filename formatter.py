def format_title(msg: str):
    formatted = "<b>" + msg + "</b>" + "\n"
    return formatted


def format_content(msg: str):
    formatted = msg + "\n"
    return formatted


def format_links(msg: str):
    formatted = "<b>Link:</b> <i>" + msg + "</i>\n"
    return formatted
