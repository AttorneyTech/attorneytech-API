from schemas.user_schema import UserSchema
from common.uri_builder import uri_builder


user_resource_type = 'users'


class UserAddress:
    '''
    This is a class for a user's address.
    '''
    def __init__(self, address_line_1, address_line_2, city, zipCode):
        self.addressLine1 = address_line_1
        self.addressLine2 = address_line_2
        self.city = city
        self.zipCode = zipCode


class UserAttribute:
    '''
    This is a class for a user's attributes.
    '''
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
    '''
    This is a class to construct a user data object for JSON API.
    '''
    def __init__(self, id, type, links, attributes):
        self.id = id
        self.type = type
        self.links = links
        self.attributes = attributes


class UserTopLevel:
    '''
    This is a class to construct a top level of resource of User for JSON API.
    '''
    def __init__(self, links, data):
        self.links = links
        self.data = data


class UserSerializer(UserAddress, UserAttribute, UserData, UserTopLevel):
    '''
    This is a multiple inheritance class to combine with the classes
    (UserAddress, UserAttribute, UserData and UserTopLevel)
    And implement the http methods, serializing or unserializing
    the response from the resource of User
    '''
    def __init__(self):
        super().__init__()
        super(UserAddress, self).__init__()
        super(UserAttribute, self).__init__()
        super(UserData, self).__init__()
        super(UserTopLevel, self).__init__()

    @staticmethod
    def serialize_user_data(user_raw_data, userId):
        '''
        Using JSON-API serializer to serialize raw data
        from the objects which were created above
        '''
        events, cases = [], []
        row = user_raw_data[0]

        if str(row[6]) not in events:
            events.append(str(row[6]))
        cases.append(str(row[7]))

        # Construct the objects of user

        user_address = UserAddress(
                            address_line_1=row[10],
                            address_line_2=row[11],
                            city=row[12],
                            zipCode=row[13]
                        )

        user_attributes = UserAttribute(
                                role=row[1],
                                username=row[2],
                                first_name=row[3],
                                middle_name=row[4],
                                last_name=row[5],
                                event_ids=events,
                                case_ids=cases,
                                email=row[8],
                                phone=row[9],
                                address=user_address
                            )

        user_data = UserData(
                            id=userId,
                            type="users",
                            links={
                                    "self": uri_builder(
                                            f'{user_resource_type}/{userId}'
                                        )
                                },
                            attributes=user_attributes
                        )

        user_top_level = UserTopLevel(
                                links={
                                        "self": uri_builder(
                                            f'{user_resource_type}/{userId}'
                                        )
                                    },
                                data=user_data
                            )

        user_response_json_api = UserSchema().dump(user_top_level)

        return user_response_json_api