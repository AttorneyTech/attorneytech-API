from typing import List

from common.openapi_loader import filter_enums


def enums_check(filters: str, endpoint: str):
    '''
    Check if the filter is valid.
    '''
    details = []
    for filter, enum in filter_enums[endpoint].items():
        if filter in filters and filters[filter] not in enum:
            details.append(
                f'''
                Invalid query parameter at {filter}: {filters[filter]}, \
                the filter must be in {enum}.
                '''
            )
    if details:
        raise ValueError(details)
    return


def filters_to_list(filters: str, data_type=None, default_value=None) -> List:
    '''
    Support for array query parameters. Process the received comma separated
    query parameter and convert it into a processable list.

    :params filter: The raw filter in comma separated format.
    :params data_type:
        If `data_type` is provided and is a callable it should convert the
        value and append it into result otherwise will append the default.
    :params default:
        The default value to be returned if the value can't be converted.
    '''
    result = []
    if filters:
        filters = filters.split(',')
        for filter in filters:
            if data_type is not None:
                try:
                    result.append(data_type(filter))
                except ValueError:
                    result.append(default_value)
            else:
                result.append(filter)
    return result
