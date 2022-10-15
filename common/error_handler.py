def error_handler(error_objects: list) -> dict:
    '''
    Serialize the error response
    '''

    error_response = {
        'errors': error_objects
    }
    return error_response


# 400 Bad request
def bad_request(details: list) -> list:
    error_objects = []
    for detail in details:
        error_objects.append(
            {
                'status': '400',
                'title': 'Bad Request',
                'detail': detail
            }
        )
    return error_objects


# 401 Unauthorized
def unauthorized(detail: str) -> list:
    error_object = [
        {
            'status': '401',
            'title': 'Unauthorized',
            'detail': detail
        }
    ]
    return error_object


# 404 Not Found
def not_found(detail: str) -> list:
    error_object = [
        {
            'status': '404',
            'title': 'Not Found',
            'detail': detail
        }
    ]
    return error_object


# 409 Conflict
def conflict(detail: str) -> list:
    error_object = [
        {
            'status': '409',
            'title': 'Conflict',
            'detail': detail
        }
    ]
    return error_object


# 500 Internal Server Error
def internal_server_error(detail: str) -> list:
    error_object = [
        {
            'status': '500',
            'title': 'Internal Server Error',
            'detail': detail
        }
    ]
    return error_object
