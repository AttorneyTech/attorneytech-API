from marshmallow import Schema, fields


class TopLevel(Schema):
    links = fields.Nested(UserSchema)
    data = fields.Nested(UserSchema)
