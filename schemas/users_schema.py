from marshmallow import Schema, fields


class UserAddressSchema(Schema):
    '''
    Defines the address object schema of user
    '''
    addressLine1 = fields.Str()
    addressLine2 = fields.Str()
    city = fields.Str()
    zipCode = fields.Str()


class UserAttributeSchema(Schema):
    '''
    Defines the attribute object schema of user
    '''
    role = fields.Str()
    username = fields.Str()
    firstName = fields.Str()
    middleName = fields.Str()
    lastName = fields.Str()
    eventIds = fields.List(fields.Str())
    caseIds = fields.List(fields.Str())
    email = fields.Email()
    phone = fields.Str()
    address = fields.Nested(UserAddressSchema)


class UserDataSchema(Schema):
    '''
    Defines the data object schema of user
    '''
    id = fields.Str()
    type = fields.Str()
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    attributes = fields.Nested(UserAttributeSchema)


class UserSchema(Schema):
    '''
    Defines the top level object schema of user
    '''
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    data = fields.Nested(UserDataSchema)


class UsersSchema(Schema):
    '''
    Defines the top level object schema of users
    '''
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    data = fields.List(fields.Nested(UserDataSchema))