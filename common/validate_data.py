from db.users_dao import UsersDao
from schemas.users_schema import UserPostSchema


def validate_post_user(post_data):
    '''
    First using he marshmallow module to check if the format or something
    missed in post data according to the schema of users.
    '''

    try:
        dao = UsersDao()
        post_data = UserPostSchema().load(post_data)
        post_email = post_data['data']['attributes']['email']
        has_result = dao.check_user_email(post_email)
        if has_result:
            dup_email = has_result['email']
            raise Exception(f'The email: {dup_email} of user already exists.')
        post_username = post_data.get('data').get('attributes').get('username')
        if post_username:
            has_result = dao.check_user_username(post_username)
            if has_result:
                dup_username = has_result['username']
                raise Exception(
                    f'The username: {dup_username} has been used.'
                )
    except Exception as err:
        raise err
