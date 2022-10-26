def get_users_filter(filter: str) -> str:
    '''
    $1 - $4 are the query parameters.
    :$1 users.role column, data type: varchar.
    :$2 users.city column, data type: varchar
    :$3 event_ids column, data type: integer.
    :$4 case_ids column, data type: integer.
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
                ELSE {param} IS NULL
            END
        '''
    elif filter in ['event_id', 'case_id']:
        return f'''
            CASE
                WHEN NULLIF({param}, ARRAY[]::integer[]) = {param}
                    THEN {filter} = ANY({param})
                ELSE true
            END
        '''


get_users_functions = {
    'get_users_filter': get_users_filter
}
get_users_statements = {
    'select_columns': '''
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
    'three_way_join': '''
        LEFT JOIN cases_users
            ON cases_users.user_id = users.id
        LEFT JOIN cases
            ON cases_users.case_id = cases.id
    ''',
    'filter_subquery': '''
        SELECT DISTINCT
            cases_users.user_id
        FROM cases_users
        LEFT JOIN cases
        ON cases.id = cases_users.case_id
    '''
}
prepare_statements = {
    # GET /users/{userId}
    'get_user_by_id': f'''
        PREPARE get_user_by_id(integer) AS
        {get_users_statements['select_columns']}
        {get_users_statements['three_way_join']}
        WHERE users.id = $1
    ''',
    # GET /users
    'get_users': f'''
        PREPARE get_users(varchar, varchar, integer[], integer[]) AS
        {get_users_statements['select_columns']}
        {get_users_statements['three_way_join']}
        WHERE users.id IN
            (
                {get_users_statements['filter_subquery']}
                WHERE {get_users_filter('case_id')}
                INTERSECT
                {get_users_statements['filter_subquery']}
                WHERE {get_users_filter('event_id')}
        )
            AND {get_users_filter('users.role')}
            AND {get_users_filter('users.city')};
    ''',
    # POST /users
    'get_user_email': '''
        PREPARE get_user_email(varchar) AS
        SELECT
            users.email
        FROM users
        WHERE users.email = $1;
    ''',
    'get_user_username': '''
        PREPARE get_user_username(varchar) AS
        SELECT
            users.username
        FROM users
        WHERE users.username = $1;
    ''',
    'get_case_ids': '''
        PREPARE get_case_ids(integer[]) AS
        SELECT
            cases.id AS case_id
        FROM cases
        WHERE cases.id = ANY($1);
    ''',
    'get_event_ids_by_case_ids': '''
        PREPARE get_event_ids_by_case_ids(integer[]) AS
        SELECT
            ARRAY_AGG(cases.event_id) AS event_ids
        FROM cases
        WHERE cases.id = ANY($1);
    ''',
    'post_user': '''
        PREPARE
            post_user(
                VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR,
                VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR
            ) AS
        INSERT INTO
            users(
                role, username, password, first_name, middle_name, last_name,
                email, phone, street_name, district, city, zip_code
            )
        VALUES(
            $1, $2, $3, $4, $5, $6,
            $7, $8, $9, $10, $11, $12
        )
        RETURNING id;
    ''',
    'post_cases_users': '''
        PREPARE
            post_cases_users(integer[], integer) AS
        INSERT INTO
            cases_users(case_id, user_id)
        VALUES
            (unnest($1), $2);
    '''
}
