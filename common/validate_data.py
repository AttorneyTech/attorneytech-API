from marshmallow import ValidationError

from db.users_dao import UsersDao
from schemas.users_schema import UserPostSchema


def validate_post_user(unchecked_data: dict) -> None | Exception:
    '''
    Checking the validation of data for creating a user.
    '''

    try:
        dao = UsersDao()
        unchecked_data = UserPostSchema().load(unchecked_data)
        email = unchecked_data['data']['attributes']['email']
        username = unchecked_data.get('data').get('attributes').get('username')
        post_case_ids = (
            unchecked_data.get('data').get('attributes').get('caseIds')
        )
        post_event_ids = (
            unchecked_data.get('data').get('attributes').get('eventIds')
        )
        # Check the email exist or not.
        has_result = dao.check_user_email(email)
        if has_result:
            dup_email = has_result['email']
            raise ValueError(
                f'The email: {dup_email} of user already exists.'
            )
        # Check the username has been used or not.
        if username is not None:
            has_result = dao.check_user_username(username)
            if has_result:
                dup_username = has_result['username']
                raise ValueError(
                    f'The username: {dup_username} has been used.'
                )
            elif username.strip() == '':
                raise ValueError('The username can not be empty.')
        # Check the cases_ids correspond to event_ids or not.
        if post_case_ids is not None and post_event_ids is not None:
            if post_case_ids == [] or post_event_ids == []:
                raise ValueError(
                    'Case_ids and event_ids can not be empty.'
                )
            case_ids, event_ids = [], []
            for item in post_case_ids:
                if not item.isdigit():
                    raise ValueError('Case id must be number.')
                case_ids.append(int(item))
            raw_case_ids = dao.check_case_ids(case_ids)
            if not raw_case_ids:
                raise ValueError('Inputted case_ids does not exist.')
            set_case_ids = set(case_ids)
            for row in raw_case_ids:
                set_case_ids.remove(row['case_id'])
            if set_case_ids:
                raise ValueError(
                    f'Inputted case_ids: {set_case_ids} does not exist.'
                )
            for item in post_event_ids:
                if not item.isdigit():
                    raise ValueError('Event id must be number.')
                event_ids.append(int(item))
            result = dao.check_user_case_and_event(case_ids)
            if not result['event_ids']:
                raise ValueError('Inputted case_ids does not exist.')
    except ValidationError as err:
        raise err
    except ValueError as err:
        raise err
    except Exception as err:
        raise err
