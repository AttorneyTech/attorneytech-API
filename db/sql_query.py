def prepare_user_query():
    prepare_statement = '''
        PREPARE get_user_by_id(integer) AS
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
        WHERE users.id = $1;
    '''

    return prepare_statement


# def user_verify_query(username):
#     user_verify_query = f'''
#         SELECT
#             users.username,
#             users.password
#         FROM users
#         WHERE users.username = '{username}';
#     '''

#     return user_verify_query
