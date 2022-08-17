def user_query(userId):
    user_query = f'''
                    SELECT
                    users.id AS user_id,
                    users.role,
                    users.username,
                    users.first_name,
                    users.middle_name,
                    users.last_name,
                    events.id AS event_id,
                    cases.id AS cases_id,
                    users.email,
                    users.phone,
                    users.street_name,
                    users.district,
                    users.city,
                    users.zip_code
                    FROM users
                    LEFT JOIN cases
                    ON users.id=cases.client_id or users.id=cases.agent_id
                    LEFT JOIN events
                    ON cases.event_id=events.id
                    WHERE users.id={userId};
                    '''
    return user_query
