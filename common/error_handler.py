def error_handler(error_objects: list) -> dict:
    '''
    Serialize the error response
    '''

    error_response = {
        'errors': error_objects
    }
    return error_response


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


def internal_server_error(detail: list) -> list:
    error_object = [
        {
            'status': '500',
            'title': 'Internal Server Error',
            'detail': detail
        }
    ]
    return error_object


def not_found(detail: list) -> list:
    error_object = [
        {
            'status': '404',
            'title': 'Not Found',
            'detail': detail
        }
    ]
    return error_object


def unauthorized(detail: list) -> list:
    error_object = [
        {
            'status': '401',
            'title': 'Unauthorized',
            'detail': detail
        }
    ]
    return error_object
