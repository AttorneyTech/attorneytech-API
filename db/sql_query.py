prepare_statement = [
    # Get /users and get /users/{userId}
    '''
    PREPARE get_users(varchar, varchar, integer, integer, integer) AS
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
        cases.id AS cases_id
    FROM users
    LEFT JOIN cases
    ON users.id = cases.client_id OR users.id = cases.agent_id
    LEFT JOIN events
    ON cases.event_id = events.id
    WHERE
    case
        WHEN NULLIF($1, NULL) = $1 THEN users.role = $1
        ELSE true
    END
    and
    case
        WHEN NULLIF($2, NULL) = $2 THEN users.city = $2
        ELSE true
    END
    and
    case
        WHEN NULLIF($3, NULL) = $3 THEN events.id = $3
        ELSE true
    END
    and
    case
        WHEN NULLIF($4, NULL) = $4 THEN cases.id = $4
        ELSE true
    END
    and
    case
        WHEN NULLIF($5, NULL) = $5 THEN users.id = $5
        ELSE true
    END;
'''
]
