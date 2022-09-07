from flask import jsonify


class ErrorHandler:
    def error_response(self):
        '''
        Serialize the error response
        '''
        error = jsonify(
            {
                "errors": [
                    {
                        "status": self.status,
                        "title": self.title,
                        "detail": self.detail
                    }
                ]
            }
        )
        return error


class InternalServerError(ErrorHandler):
    def __init__(self, detail):
        self.status = '500'
        self.title = 'Internal Server Error'
        self.detail = detail

    def error_response(self):
        return super().error_response()


class NotFound(ErrorHandler):
    def __init__(self, detail):
        self.status = '404'
        self.title = 'Not Found'
        self.detail = detail

    def error_response(self):
        return super().error_response()


class Unauthorized(ErrorHandler):
    def __init__(self, detail):
        self.status = '401'
        self.title = 'Unauthorized'
        self.detail = detail

    def error_response(self):
        return super().error_response()
