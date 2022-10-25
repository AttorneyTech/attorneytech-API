from marshmallow import fields, Schema, validate
from common.openapi_loader import enums


class UserAddressSchema(Schema):
    '''Defines the address object schema of user'''

    addressLine1 = fields.Str(validate=[validate.Length(max=100)])
    addressLine2 = fields.Str(validate=[validate.Length(max=20)])
    city = fields.Str(
        validate=[
            validate.Length(max=20),
            validate.OneOf(enums['users']['filter[city]'])
        ]
    )
    zipCode = fields.Str(validate=[validate.Length(max=10)])


class UserAttributeSchema(Schema):
    '''Defines the attribute object schema of user'''

    role = fields.Str(
        required=True,
        validate=validate.OneOf(enums['users']['filter[role]'])
    )
    username = fields.Str(validate=[validate.Length(max=20)])
    firstName = fields.Str(required=True, validate=[validate.Length(max=50)])
    middleName = fields.Str(validate=[validate.Length(max=50)])
    lastName = fields.Str(required=True, validate=[validate.Length(max=50)])
    eventIds = fields.List(fields.Str())
    caseIds = fields.List(fields.Str())
    email = fields.Email(
        required=True,
        validate=[validate.Length(max=50), validate.Email()]
    )
    phone = fields.Str(validate=[validate.Length(max=10)])
    address = fields.Nested(UserAddressSchema)
    password = fields.Str(validate=[validate.Length(min=6, max=36)])


class UserDataSchema(Schema):
    '''Defines the data object schema of user'''

    id = fields.Str()
    type = fields.Str()
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    attributes = fields.Nested(UserAttributeSchema(exclude=('password',)))


class UserPostDataSchema(Schema):
    '''Defines the data object schema of user'''

    id = fields.Str()
    type = fields.Str()
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    attributes = fields.Nested(UserAttributeSchema)


class UserSchema(Schema):
    '''Defines the top level object schema of user'''

    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    data = fields.Nested(UserDataSchema)


class UserPostSchema(Schema):
    '''Defines the top level object schema of user'''

    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    data = fields.Nested(UserPostDataSchema)


class UsersSchema(Schema):
    '''Defines the top level object schema of users'''

    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    data = fields.List(fields.Nested(UserDataSchema))
