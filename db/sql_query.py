from string import Template


single_filter = Template(
    '''
    CASE
        WHEN NULLIF(%($value)s, NULL) = %($value)s
            THEN $filter = %($value)s
        ELSE %($value)s IS NULL
    END
    '''
)
list_filter = Template(
    '''
    CASE
        WHEN NULLIF(%($value)s, ARRAY[]::integer[]) = %($value)s
            THEN $filter = ANY(%($value)s)
        ELSE $boolean
    END
    '''
)


# Define the functions of conditional statement
def users_filters(filter: str, value) -> str:
    if filter in ['users.role', 'users.city']:
        filter_statement = single_filter.substitute(
            filter=filter, value=value
        )
        return filter_statement
    elif filter in ['cases.event_id', 'cases.id']:
        filter_statement = list_filter.safe_substitute(
            filter=filter, value=value
        )
        filter_statement = Template(filter_statement)
        return filter_statement


select_user_column = '''
    SELECT
        users.id AS user_id,
        users.role,
        users.username,
        users.first_name,
        users.middle_name,
        users.last_name,
        users.email,
        users.phone,
        users.street_name,
        users.district,
        users.city,
        users.zip_code,
        cases.event_id AS event_id,
        cases_users.case_id
    FROM users
    '''
user_join_tables = '''
    LEFT JOIN cases_users
        ON cases_users.user_id = users.id
    LEFT JOIN cases
        ON cases_users.case_id = cases.id
    '''


def select_users(event_ids: list, case_ids: list):
    role_filter = users_filters(filter='users.role', value='role')
    city_filter = users_filters(filter='users.city', value='city')
    case_id_filter = users_filters(filter='cases.id', value='case_ids')
    event_id_filter = users_filters(filter='cases.event_id', value='event_ids')
    if event_ids or case_ids:
        case_id_filter = case_id_filter.substitute(boolean='false')
        event_id_filter = event_id_filter.substitute(boolean='false')
    else:
        case_id_filter = case_id_filter.substitute(boolean='true')
        event_id_filter = event_id_filter.substitute(boolean='true')
    return f'''
        {select_user_column}
        {user_join_tables}
        WHERE users.id IN
            (
                SELECT DISTINCT
                    user_id
                FROM cases_users
                WHERE case_id IN (
                    SELECT cases.id
                    FROM cases
                    WHERE {case_id_filter}
                    OR {event_id_filter}
                )
            )
            AND {role_filter}
            AND {city_filter};
        '''


prepare_statements = {
    # GET /users/{userId}
    'get_user_by_id': f'''
        PREPARE get_user_by_id(integer) AS
        {select_user_column}
        {user_join_tables}
        WHERE users.id = $1
        '''
}
