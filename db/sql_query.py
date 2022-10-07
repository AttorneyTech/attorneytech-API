# Define the functions of conditional statement
def get_users_with_filter(filter: str) -> str:
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
        'cases.event_id': '$3',
        'cases.id': '$4'
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


reusable_func = {
    'get_users': get_users_with_filter
}

reusable_statement = {
    'select_user_column': '''
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
        ''',
    'user_join_tables': '''
        LEFT JOIN cases_users
            ON cases_users.user_id = users.id
        LEFT JOIN cases
            ON cases_users.case_id = cases.id
        '''
}

prepare_statements = {
    # GET /users/{userId}
    'get_user_by_id': f'''
        PREPARE get_user_by_id(integer) AS
        {reusable_statement['select_user_column']}
        {reusable_statement['user_join_tables']}
        WHERE users.id = $1
        ''',
    # GET /users
    'get_users': f'''
        PREPARE get_users(varchar, varchar, integer[], integer[]) AS
        {reusable_statement['select_user_column']}
        {reusable_statement['user_join_tables']}
        WHERE users.id IN
            (
                SELECT DISTINCT
                    user_id
                FROM cases_users
                WHERE case_id IN (
                    SELECT cases.id
                    FROM cases
                    WHERE {reusable_func['get_users']('cases.event_id')}
                        AND {reusable_func['get_users']('cases.id')}
                )
                AND {reusable_func['get_users']('users.role')}
                AND {reusable_func['get_users']('users.city')}
            );
        '''
}
