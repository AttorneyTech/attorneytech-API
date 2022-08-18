from marshmallow import Schema, fields


class UserAddress:
    def __init__(self, address_line_1, address_line_2, city, zipCode):
        self.addressLine1 = address_line_1
        self.addressLine2 = address_line_2
        self.city = city
        self.zipCode = zipCode


class UserAttribute:
    def __init__(
                self, role, username, first_name, middle_name, last_name,
                event_ids, case_ids, email, phone, address
            ):
        self.role = role
        self.username = username
        self.firstName = first_name
        self.middleName = middle_name
        self.lastName = last_name
        self.eventIds = event_ids
        self.caseIds = case_ids
        self.email = email
        self.phone = phone
        self.address = address


class UserData:
    def __init__(self, id, type, links, attributes):
        self.id = id
        self.type = type
        self.links = links
        self.attributes = attributes


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
