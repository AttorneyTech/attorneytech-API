from textwrap import dedent


def string_handler(raw_string):
    string = dedent(
        str(raw_string)
        ).replace('\"', '').replace('\n', '').replace('  ', '')

    return string
