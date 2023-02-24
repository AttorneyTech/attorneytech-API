from typing import List, Union

from marshmallow import ValidationError

from common.custom_exception import CustomBadRequestError, CustomConflictError
from schemas.users_schema import UserPostSchema


def validate_email_username(
    dao: object, email: str, username: str
) -> None | CustomConflictError:
    '''Check the email exist or not.'''

    if username is not None and username.isspace():
        raise CustomConflictError('The username cannot be empty.')

    raw_result = dao.get_email_username(email, username)

    if raw_result:
        for row in raw_result:
            if row['email'] == email:
                raise CustomConflictError(
                    f'The email: {email} of user already exists.'
                )
            else:
                if row['username'] == username:
                    raise CustomConflictError(
                        f'The username: {username} has been used.'
                    )


def validate_cases_ids(
    dao: object, post_case_ids: List[str]
) -> Union[list, CustomBadRequestError, CustomConflictError]:
    '''
    Check if the inputted cases_ids exist in database.
    If the `post_case_ids` is valid, convert it to int of list
    and return it as `case_ids`.
    '''

    case_ids = []
    for item in post_case_ids:
        if not item.isdigit():
            raise CustomBadRequestError('Case id must be a digit string.')
        case_ids.append(int(item))

    raw_case_ids = dao.get_case_ids(case_ids)

    if not raw_case_ids:
        raise CustomBadRequestError('Inputted case_ids does not exist.')

    diff_set = set(case_ids) - set([row['case_id'] for row in raw_case_ids])

    if diff_set:
        raise CustomBadRequestError(
            f'Inputted case_ids: {diff_set} does not exist.'
        )
    return case_ids


def validate_events_cases(
    dao: object, post_event_ids: List[str], case_ids: list
) -> Union[None, CustomBadRequestError, CustomConflictError]:
    '''Check the cases_ids correspond to event_ids or not.'''

    event_ids = []
    for item in post_event_ids:
        if not item.isdigit():
            raise CustomBadRequestError('Event id must be a digit string.')

        event_ids.append(int(item))

    result = dao.get_event_ids_by_case_ids(case_ids)
    result_event_ids = set(result['event_ids'])
    input_event_ids = set(event_ids)

    if result_event_ids != input_event_ids:
        invalid_event_ids = result_event_ids.intersection(input_event_ids)
        raise CustomConflictError(
            f'''
            Inputted event_ids: {invalid_event_ids} can not be matched.
            '''
        )


def validate_user_data(
    dao: object, raw_data: dict, patch: bool
) -> Union[dict, list, None, Exception]:
    '''
    Checking the validation of data for creating a user.
    The marshmallow module will check if the raw_data has something
    required but missed, and basic format of data. If there are something
    invalid, will raise ValidationError.
    After that return `unchecked_data` to check if in conflict with the
    resources. If something invalid, will raise CustomConflictError.
    '''

    try:
        if patch:
            unchecked_data = UserPostSchema().load(raw_data, partial=True)
        else:
            unchecked_data = UserPostSchema().load(raw_data)

        email = unchecked_data.get('data').get('attributes').get('email')
        username = unchecked_data.get('data').get('attributes').get('username')
        post_case_ids = (
            unchecked_data.get('data').get('attributes').get('caseIds')
        )
        post_event_ids = (
            unchecked_data.get('data').get('attributes').get('eventIds')
        )
        validate_email_username(dao, email, username)

        if post_case_ids is None and post_event_ids is None:
            return unchecked_data, None
        elif post_case_ids is not None and post_event_ids is not None:
            if post_case_ids == [] or post_event_ids == []:
                raise CustomBadRequestError(
                    'Case_ids and event_ids cannot be empty.'
                )

            case_ids = validate_cases_ids(dao, post_case_ids)
            validate_events_cases(dao, post_event_ids, case_ids)
            return unchecked_data, case_ids
        else:
            raise CustomConflictError(
                'Case_ids and event_ids must be correspond to each other.'
            )
    except (
        ValidationError, CustomBadRequestError, CustomConflictError, Exception
    ) as err:
        raise err
