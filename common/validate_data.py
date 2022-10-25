from typing import List

from marshmallow import ValidationError

from db.users_dao import UsersDao
from schemas.users_schema import UserPostSchema


def validate_user_email(dao: object, email: str) -> None | ValueError:
    '''Check the email exist or not.'''

    has_result = dao.get_user_email(email)
    if has_result:
        dup_email = has_result['email']
        raise ValueError(f'The email: {dup_email} of user already exists.')


def validate_username(dao: object, username: str) -> None | ValueError:
    '''Check the username has been used or not.'''

    if username is not None:
        has_result = dao.get_user_username(username)
        if has_result:
            dup_username = has_result['username']
            raise ValueError(f'The username: {dup_username} has been used.')
        elif username.strip() == '':
            raise ValueError('The username can not be empty.')


def validate_cases_ids(
    dao: object, post_case_ids: List[str]
) -> list | ValueError:
    '''Check if the inputted cases_ids exist in database'''

    case_ids = []
    for item in post_case_ids:
        if not item.isdigit():
            raise ValueError('Case id must be number.')
        case_ids.append(int(item))

    raw_case_ids = dao.get_case_ids(case_ids)
    if not raw_case_ids:
        raise ValueError('Inputted case_ids does not exist.')

    set_case_ids = set(case_ids)
    for row in raw_case_ids:
        set_case_ids.remove(row['case_id'])

    if set_case_ids:
        raise ValueError(f'Inputted case_ids: {set_case_ids} does not exist.')

    return case_ids


def validate_events_with_cases(
    dao: object, post_event_ids: List[str], case_ids: list
) -> None | ValueError:
    '''Check the cases_ids correspond to event_ids or not.'''

    event_ids = []
    for item in post_event_ids:
        if not item.isdigit():
            raise ValueError('Event id must be number.')
        event_ids.append(int(item))

    result = dao.get_event_ids_by_case_ids(case_ids)
    result_event_ids = set(result['event_ids'])
    input_event_ids = set(event_ids)
    if result_event_ids != input_event_ids:
        invalid_event_ids = result_event_ids.intersection(input_event_ids)
        raise ValueError(
            f'''
            Inputted event_ids: {invalid_event_ids} can not be matched.
            '''
        )


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
        validate_user_email(dao, email)
        validate_username(dao, username)

        if post_case_ids is not None and post_event_ids is not None:
            if post_case_ids == [] or post_event_ids == []:
                raise ValueError('Case_ids and event_ids can not be empty.')
            case_ids = validate_cases_ids(dao, post_case_ids)
            validate_events_with_cases(dao, post_event_ids, case_ids)
    except ValidationError as err:
        raise err
    except ValueError as err:
        raise err
    except Exception as err:
        raise err

# TODO:
# Validate role
# Validate city
# fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
