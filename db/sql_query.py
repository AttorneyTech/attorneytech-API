def get_users_conditional_query(filter: str) -> str:
    '''
    $1 - $4 are the placeholder of query parameters.
    :$1 For column users.role. Data type: varchar.
    :$2 For column users.city. Data type: varchar
    :$3 For column event_id. Data type: list of integer.
    :$4 For column case_id. Data type: list of integer.
    '''
    get_users_filters_dict = {
        'users.role': '$1',
        'users.city': '$2',
        'event_id': '$3',
        'case_id': '$4'
    }
    param = get_users_filters_dict[filter]

    if filter in ['users.role', 'users.city']:
        return f'''
            CASE
                WHEN NULLIF({param}, NULL) = {param}
                    THEN {filter} = {param}
                ELSE true
            END
            '''
    return f'''
        CASE
            WHEN NULLIF({param}, ARRAY[]::integer[]) = {param}
                THEN {filter} = ANY(ARRAY[{param}])
            ELSE true
        END
        '''


def user_join_tables():
    user_join_tables = '''
    LEFT JOIN cases_users
        ON cases_users.user_id = users.id
    LEFT JOIN cases
        ON cases_users.case_id = cases.id
    LEFT JOIN events
        ON cases.event_id = events.id
    '''
    return user_join_tables


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
        events.id AS event_id,
        cases_users.case_id
    FROM users
'''

prepare_statements = [
    # Get /users/{userId}
    f'''
    PREPARE get_user_by_id(integer) AS
    {select_user_column}
    {user_join_tables()}
    WHERE users.id = $1
    ''',
    # Get filtered id of users
    f'''
    PREPARE get_users(varchar, varchar, integer[], integer[]) AS
    SELECT DISTINCT
        users.id AS user_id
    FROM users
    {user_join_tables()}
    WHERE {get_users_conditional_query('users.role')}
        AND {get_users_conditional_query('users.city')}
        AND {get_users_conditional_query('event_id')}
        AND {get_users_conditional_query('case_id')};
    ''',
    # Get filtered /users
    f'''
    PREPARE get_filtered_users(integer[]) AS
    {select_user_column}
    {user_join_tables()}
    WHERE users.id = ANY(ARRAY[$1])
    '''
]
