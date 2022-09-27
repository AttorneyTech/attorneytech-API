from typing import List, Optional

from common.openapi_loader import filter_enums


def enums_check(filters: str, endpoint: str) -> bool:
    '''
    Check if the filter is valid.
    '''

    for filter, enum in filter_enums[endpoint].items():
        if filter in filters and filters[filter] not in enum:
            raise ValueError(
                f'''
                Invalid query parameter at
                 {filter}: {filters[filter]},
                 the filter must be in {enum}.
                '''
            )
    return


def filter_to_list(
    filter: str, data_type: Optional[int] = None
) -> List[int | str]:
    '''
    Support for array query parameters. Process the received comma separated
    query parameter and convert it into a processable list.

    :params filter: The raw filter in comma separated format.
    :params data_type: This parameter is to convert the type of the filter to
                       conform to a form acceptable to the database. It can be
                       `int` if needed otherwise default is `None`.
    '''

    if filter:
        result = []
        filter = filter.split(',')
        if data_type is None:
            for item in filter:
                result.append(item)
        elif data_type == int:
            for item in filter:
                # If the filter is not numbers, such as letters, etc.
                # Since this is not a valid query parameter for the database,
                # so here replace it with -1.
                if item.isdigit():
                    result.append(data_type(item))
                else:
                    result.append(-1)
        return result
    return filter
