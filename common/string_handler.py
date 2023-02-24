from textwrap import dedent


def error_detail_handler(raw_detail: str | BaseException) -> str:
    '''
    Remove any common leading whitespace from every line in string
    , replacing the backslash and blank lines.
    '''

    string = dedent(
        str(raw_detail)
    ).replace('\"', '').replace('\n', '').replace('  ', '')

    return string
