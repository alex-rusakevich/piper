from typing import Tuple


def get_line_by_char_pos(text: str, char_pos: int) -> Tuple[str, int, int]:
    line_num = text[:char_pos].count("\n")
    text_str = text.split("\n")[line_num]

    char_pos = char_pos - text_str.rfind("\n")
    return (text_str, line_num + 1, char_pos + 1)
