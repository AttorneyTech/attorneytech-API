from typing import List

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


def filter_to_list(filter: str, data_type: int | str) -> List[int | str]:
    '''
    Support for array query parameters.
    Process the received comma separated query parameter
    and convert it into a processable list.
    '''

    if filter:
        result = []
        filter = filter.split(',')
        for item in filter:
            try:
                result.append(data_type(item))
            # If the input filter is other than numbers, such as letters, etc,
            # which the data type is not valid for the database data type,
            # replace it with -1
            except ValueError:
                result.append(-1)
        return result
    return filter
