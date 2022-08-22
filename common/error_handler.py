from flask import jsonify


class InternalServerError:
    def __init__(self, detail):
        self.status = '500'
        self.title = 'Internal Server Error'
        self.detail = detail

    def error_response(self):
        error = jsonify({
                    "errors": [
                            {
                                "status": self.status,
                                "title": self.title,
                                "detail": self.detail
                            }
                        ]
                    })
        return error


class NotFound:
    def __init__(self, detail):
        self.status = '404'
        self.title = 'Not Found'
        self.detail = detail

    def error_response(self):
        error = jsonify({
                    "errors": [
                            {
                                "status": self.status,
                                "title": self.title,
                                "detail": (
                                        f'Resource of user id:'
                                        f'{self.detail} not found'
                                    )
                            }
                        ]
                    })
        return error


class UnauthorizedLogin:
    def __init__(self):
        self.status = '401'
        self.title = 'Unauthorized'
        self.detail = 'Unauthorized, invalid username or password'

    def error_response(self):
        error = jsonify({
                    "errors": [
                            {
                                "status": self.status,
                                "title": self.title,
                                "detail": self.detail
                            }
                        ]
                    })
        return error
