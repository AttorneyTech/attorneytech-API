from textwrap import dedent


users_attributes = {
    'firstName': 'first_name',
    'middleName': 'middle_name',
    'lastName': 'last_name',
    'addressLine1': 'street_name',
    'addressLine2': 'addressLine2',
    'zipCode': 'zip_code'
}


def error_detail_handler(raw_detail: str | BaseException) -> str:
    '''
    Remove any common leading whitespace from every line in string
    , replacing the backslash and blank lines.
    '''

    string = dedent(
        str(raw_detail)
    ).replace('\"', '').replace('\n', '').replace('  ', '')

    return string


def get_values(data, values):
    '''
    This function is mainly for processing strings
    verified by marshmallow.
    '''

    if isinstance(data, dict):
        for v in data.values():
            get_values(v, values)
    else:
        values.append(data[0])

    return values
