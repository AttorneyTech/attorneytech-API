from marshmallow import Schema, fields


class UserAddressSchema(Schema):
    addressLine1 = fields.Str()
    addressLine2 = fields.Str()
    city = fields.Str()
    zipCode = fields.Str()


class UserAttributeSchema(Schema):
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
    id = fields.Str()
    type = fields.Str()
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    attributes = fields.Nested(UserAttributeSchema)


class UserSchema(Schema):
    links = fields.Dict(keys=fields.Str(), values=fields.Str())
    data = fields.Nested(UserDataSchema)
