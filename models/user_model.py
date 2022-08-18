from schemas.user_schema import UserSchema


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


class UserModel(UserAddress, UserAttribute, UserData, UserTopLevel):
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
    def get_user_by_id(response, userId):
        events, cases = [], []
        row = response[0]

        if str(row[6]) not in events:
            events.append(str(row[6]))
        cases.append(str(row[7]))

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
                                    "self": f"http://127.0.0.1:5000/users/{userId}"
                                },
                            attributes=user_attributes
                        )

        user_top_level = UserTopLevel(
                                links={
                                        "self": f"http://127.0.0.1:5000/users/{userId}"
                                    },
                                data=user_data
                            )

        result = UserSchema().dump(user_top_level)

        return result
