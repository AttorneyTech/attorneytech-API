from common.openapi_loader import filter_enums


def valid_filters(filters, endpoint):
    '''
    Check if the filter is valid.
    '''

    # Enums checking
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


def filter_to_list(filter):
    if filter:
        try:
            result = []
            filter = filter.split(',')
            for item in filter:
                result.append(int(item))
        except ValueError:
            pass
        return result
    return filter
