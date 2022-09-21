enums = {
    'users': {
        'filter[role]': ['agent', 'client'],
        'filter[city]': [
            '臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市', '新竹縣', '苗栗縣', '彰化縣',
            '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣',
            '連江縣', '基隆市', '新竹市', '嘉義市'
        ]
    }
}

data_types = {
    'users': {
        'filter[eventIds][oneOf]': int,
        'filter[caseIds][oneOf]': int
    }
}


def valid_filters(filters, endpoint):
    '''
    Check if the filter is in enums and the data type is valid.
    '''

    # Enums checking
    for filter, enum in enums[endpoint].items():
        if filter in filters and filters[filter] not in enum:
            raise ValueError(
                f'''
                Invalid query parameter at
                 {filter}: {filters[filter]},
                 the filter must be in {enum}.
                '''
            )
    # Data type checking.
    for filter in data_types[endpoint].keys():
        if filter in filters:
            filters_dict = filters.to_dict(flat=False)
            for v in filters_dict[filter]:
                try:
                    int(v)
                except ValueError:
                    raise ValueError(
                        f'''
                        Invalid query parameter at
                         {filter}: {filters[filter]},
                         the data type of filter must be
                         {data_types[endpoint][filter]}.
                        '''
                    )
    return
