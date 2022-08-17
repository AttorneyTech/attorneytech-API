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
    def __init__(self):
        self.status = '404'
        self.title = 'Not Found'
        self.detail = 'Resource not found'

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
