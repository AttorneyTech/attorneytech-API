from db.users_dao import UsersDao
from schemas.users_schema import UserPostSchema


def validate_post_user(post_data: dict) -> None | Exception:
    '''
    Using marshmallow module to check if the format or something
    that required but missed in post data according to the schema of users.

    And check by email if the users that want to create already exist, finally
    suppose there is an input username in the post data, check whether the
    username has been used.
    '''

    try:
        dao = UsersDao()
        post_data = UserPostSchema().load(post_data)
        post_email = post_data['data']['attributes']['email']
        # Check the email exist or not.
        has_result = dao.check_user_email(post_email)
        if has_result:
            dup_email = has_result['email']
            raise Exception(f'The email: {dup_email} of user already exists.')
        # Check the username has been used or not.
        post_username = post_data.get('data').get('attributes').get('username')
        if post_username is not None:
            has_result = dao.check_user_username(post_username)
            if has_result:
                dup_username = has_result['username']
                raise Exception(
                    f'The username: {dup_username} has been used.'
                )
            elif not post_username.strip():
                raise Exception('The username can not be empty.')
    except Exception as err:
        raise err
