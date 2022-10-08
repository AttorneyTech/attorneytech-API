# Define the functions of conditional statement
def users_filters(filter: str, value) -> str:
    if filter in ['users.role', 'users.city']:
        return f'''
            CASE
                WHEN NULLIF({value}, NULL) = {value}
                    THEN {filter} = {value}
                ELSE {value} IS NULL
            END
            '''
    return f'''
        CASE
            WHEN NULLIF({value}, ARRAY[]::integer[]) = {value}
                THEN {filter} = ANY(ARRAY[{value}])
            ELSE false
        END
        '''


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


def select_users(role, city, event_ids, case_ids):
    if event_ids or case_ids:
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
                        WHERE {
                            users_filters(
                                filter='cases.event_id', value=event_ids
                            )
                        }
                        OR {
                            users_filters(
                                filter='cases.id', value=case_ids
                            )
                        }
                    )
                )
                AND {
                    users_filters(
                        filter='users.role', value=role
                    )
                }
                AND {
                    users_filters(
                        filter='users.city', value=city
                    )
                };
            '''
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
                    )
                )
                AND {
                    users_filters(
                        filter='users.role', value=role
                    )
                }
                AND {
                    users_filters(
                        filter='users.city', value=city
                    )
                };
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
