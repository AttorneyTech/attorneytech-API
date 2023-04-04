from typing import Union


def error_top_level(error_objects: list) -> Union[dict, int]:
    '''
    Serialize the error response
    '''

    error_response = {
        'errors': error_objects
    }
    return error_response


# 400 Bad request
def bad_request(details: list) -> Union[dict, int]:
    error_objects = []
    for detail in details:
        error_objects.append(
            {
                'status': '400',
                'title': 'Bad Request',
                'detail': detail
            }
        )
    error_response = error_top_level(error_objects)
    return error_response, 400


# 401 Unauthorized
def unauthorized(detail: str) -> Union[dict, int]:
    error_object = [
        {
            'status': '401',
            'title': 'Unauthorized',
            'detail': detail
        }
    ]
    error_response = error_top_level(error_object)
    return error_response, 401


# 404 Not Found
def not_found(detail: str) -> Union[dict, int]:
    error_object = [
        {
            'status': '404',
            'title': 'Not Found',
            'detail': detail
        }
    ]
    error_response = error_top_level(error_object)
    return error_response, 404


def user_not_found(user_id):
    detail = (
        f'The resource requested (user ID: {user_id}) not found.'
    )
    error_response, error_code = not_found(detail)
    return error_response, error_code, detail


# 409 Conflict
def conflict(detail: str) -> Union[dict, int]:
    error_object = [
        {
            'status': '409',
            'title': 'Conflict',
            'detail': detail
        }
    ]
    error_response = error_top_level(error_object)
    return error_response, 409


# 500 Internal Server Error
def internal_server_error(detail: str) -> Union[dict, int]:
    error_object = [
        {
            'status': '500',
            'title': 'Internal Server Error',
            'detail': detail
        }
    ]
    error_response = error_top_level(error_object)
    return error_response, 500


error_names = {
    'CustomConflictError': conflict
}
