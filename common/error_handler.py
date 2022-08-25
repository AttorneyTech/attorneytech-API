from flask import jsonify


class ErrorHandler:
    def __init__(self):
        pass

    def error_response(self):
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


class NotFound(ErrorHandler):
    def __init__(self, detail):
        self.status = '404'
        self.title = 'Not Found'
        self.detail = detail


class UnauthorizedLogin(ErrorHandler):
    def __init__(self):
        self.status = '401'
        self.title = 'Unauthorized'
        self.detail = 'Unauthorized, invalid username or password'
