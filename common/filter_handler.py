from typing import List, Optional

from common.openapi_loader import filter_enums


def enums_check(filters: str, endpoint: str):
    '''
    Check if the filter is valid.
    '''

    for filter, enum in filter_enums[endpoint].items():
        if filter in filters and filters[filter] not in enum:
            raise ValueError(
                f'''
                Invalid query parameter at {filter}: {filters[filter]}, \
                the filter must be in {enum}.
                '''
            )
    return


def filters_to_list(
    filters: str, data_type: Optional[int] = None
) -> List[int | str]:
    '''
    Support for array query parameters. Process the received comma separated
    query parameter and convert it into a processable list.

    :params filter: The raw filter in comma separated format.
    :params data_type: This parameter is to convert the type of the filter to
                       conform to a form acceptable to the database. It can be
                       `int` if needed otherwise default is `None`.
    '''
    result = []
    if filters:
        filters = filters.split(',')
        for filter in filters:
            if data_type == int:
                result.append(data_type(filter) if filter.isdigit() else -1)
            else:
                result.append(filter)
    return result
