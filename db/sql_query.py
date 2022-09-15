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
    get_users_filters_dict = {
        'users.role': '$1',
        'users.city': '$2',
        'event_ids': '$3',
        'case_ids': '$4',
        'users.id': '$5',
    }
    param = get_users_filters_dict[filter]

    return f'''
    CASE
        WHEN NULLIF({param}, NULL) = {param} THEN {filter} = {param}
        ELSE true
    END
    ''' if filter in ['users.role', 'users.city', 'users.id'] \
        else f'''
    CASE
        WHEN NULLIF({param}, ARRAY[]::integer[]) = {param}
            THEN ARRAY[{param}] && {filter}
        ELSE true
    END
    '''


prepare_statements = [
    # Get /users and get /users/{userId}
    f'''
    PREPARE get_users(varchar, varchar, integer[], integer[], integer) AS
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
    WHERE {get_users_conditional_query('users.role')}
        AND {get_users_conditional_query('users.city')}
        AND {get_users_conditional_query('event_ids')}
        AND {get_users_conditional_query('case_ids')}
        AND {get_users_conditional_query('users.id')};
    '''
]
