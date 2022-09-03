from schemas.user_schema import UserSchema
from common.uri_builder import uri_builder


user_resource_type = 'users'


class UserAddress:
    '''
    Construct address object of a user
    '''
    def __init__(
        self,
        address_line_1,
        address_line_2,
        city,
        zipCode
    ):
        self.addressLine1 = address_line_1
        self.addressLine2 = address_line_2
        self.city = city
        self.zipCode = zipCode


class UserAttribute:
    '''
    Construct attributes object of a user
    '''
    def __init__(
        self,
        role,
        username,
        first_name,
        middle_name,
        last_name,
        event_ids,
        case_ids,
        email,
        phone,
        address
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
    Construct data object of a user
    '''
    def __init__(
        self,
        id,
        type,
        links,
        attributes
    ):
        self.id = id
        self.type = type
        self.links = links
        self.attributes = attributes


class UserTopLevel:
    '''
    Construct top level object of a user in JSON:API format
    '''
    def __init__(self, links, data):
        self.links = links
        self.data = data


class UserSerializer(UserAddress, UserAttribute, UserData, UserTopLevel):
    '''
    Combine with the objects of Users and
    construct the serializer for user resource
    '''
    def __init__(self):
        super().__init__()
        super(UserAddress, self).__init__()
        super(UserAttribute, self).__init__()
        super(UserData, self).__init__()
        super(UserTopLevel, self).__init__()

    @staticmethod
    def serialize_raw_user(raw_user):
        '''
        Serializes raw user data from user resource
        '''
        events, cases = [], []

        # Compose the events and cases list
        # and deal with the duplicate events in each row
        for row in raw_user:
            if row['event_id'] not in events:
                events.append(row['event_id'])
            cases.append(row['cases_id'])

        # Compose the rest part of user data
        # and here use the first dict of raw user
        row = raw_user[0]
        user_address_object = UserAddress(
            address_line_1=row['street_name'],
            address_line_2=row['district'],
            city=row['city'],
            zipCode=row['zip_code']
        )

        user_attributes_object = UserAttribute(
            role=row['role'],
            username=row['username'],
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            event_ids=events,
            case_ids=cases,
            email=row['email'],
            phone=row['phone'],
            address=user_address_object
        )

        user_data_object = UserData(
            id=row['user_id'],
            type=user_resource_type,
            links={
                'self': uri_builder(f'{user_resource_type}/{row["user_id"]}')
            },
            attributes=user_attributes_object
        )

        user_response = UserTopLevel(
            links={
                'self': uri_builder(f'{user_resource_type}/{row["user_id"]}')
            },
            data=user_data_object
        )

        user_response_json = UserSchema().dump(user_response)

        return user_response_json
