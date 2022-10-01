from textwrap import dedent


def error_detail_handler(raw_detail: str | BaseException) -> str:
    string = dedent(
        str(raw_detail)
    ).replace('\"', '').replace('\n', '').replace('  ', '')

    return string
