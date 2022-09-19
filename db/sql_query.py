def union_events_and_cases(role: str) -> str:
    user_role_dict = {
        'agent': 'agent_id',
        'client': 'client_id'
    }
    param = user_role_dict[role]

    return f'''
    SELECT cases.{param} AS user_id,
    ARRAY_AGG(DISTINCT events.id) AS event_ids,
    ARRAY_AGG(cases.id) AS case_ids
    FROM cases
    RIGHT JOIN events
    ON cases.event_id = events.id
    GROUP BY cases.{param}
    '''


def get_users_conditional_query(filter: str) -> str:
    '''
    :$1 Query parameter placeholder of users.role,
    the data type pass into db is varchar.
    :$2 Query parameter placeholder of users.city,
    the data type pass into db is varchar
    :$3 Query parameter placeholder of event_ids,
    the data type pass into db is array of integer.
    :$4 Query parameter placeholder of case_ids,
    the data type pass into db is array of integer.
    '''
    get_users_filters_dict = {
        'users.role': '$1',
        'users.city': '$2',
        'event_ids': '$3',
        'case_ids': '$4'
    }
    param = get_users_filters_dict[filter]

    return f'''
    CASE
        WHEN NULLIF({param}, NULL) = {param} THEN {filter} = {param}
        ELSE true
    END
    ''' if filter in ['users.role', 'users.city'] \
        else f'''
    CASE
        WHEN NULLIF({param}, ARRAY[]::integer[]) = {param}
            THEN ARRAY[{param}] && {filter}
        ELSE true
    END
    '''


# Select columns in users table and union of events and cases
# This SQL statement will be reused in get /users and /users/{userId}
construct_user_column = f'''
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
        event_ids,
        case_ids
    FROM users
    LEFT JOIN
    (
        {union_events_and_cases('agent')}
        UNION
        {union_events_and_cases('client')}
    ) AS users_events_cases
    ON
    users.id = users_events_cases.user_id
'''


prepare_statements = [
    # Get /users/{userId}
    f'''
    PREPARE get_user_by_id(integer) AS
    {construct_user_column}
    WHERE users.id = $1
    ''',
    # Get /users
    f'''
    PREPARE get_users(varchar, varchar, integer[], integer[]) AS
    {construct_user_column}
    WHERE {get_users_conditional_query('users.role')}
        AND {get_users_conditional_query('users.city')}
        AND {get_users_conditional_query('event_ids')}
        AND {get_users_conditional_query('case_ids')};
    '''
]
