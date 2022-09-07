from common.uri_builder import uri_builder
from schemas.user_schema import UserSchema


# Type of user resource
user_resource_type = 'users'


class UserAddress:
    '''
    Construct address object of a user
    '''
    def __init__(self, user_address):
        self.addressLine1 = user_address['address_line_1']
        self.addressLine2 = user_address['address_line_2']
        self.city = user_address['city']
        self.zipCode = user_address['zip_code']


class UserAttribute:
    '''
    Construct attributes object of a user
    '''
    def __init__(self, user_attributes):
        self.role = user_attributes['role']
        self.username = user_attributes['username']
        self.firstName = user_attributes['first_name']
        self.middleName = user_attributes['middle_name']
        self.lastName = user_attributes['last_name']
        self.eventIds = user_attributes['event_ids']
        self.caseIds = user_attributes['case_ids']
        self.email = user_attributes['email']
        self.phone = user_attributes['phone']
        self.address = user_attributes['address']


class UserData:
    '''
    Construct data object of a user
    '''
    def __init__(self, user_data):
        self.id = user_data['id']
        self.type = user_data['type']
        self.links = user_data['links']
        self.attributes = user_data['attributes']


class UserTopLevel:
    '''
    Construct top level object of a user in JSON:API format
    '''
    def __init__(self, user_object):
        self.links = user_object['links']
        self.data = user_object['data']


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

        # Compose the address object of user
        user_address = {
            'address_line_1': row['street_name'],
            'address_line_2': row['district'],
            'city': row['city'],
            'zip_code': row['zip_code']
        }
        user_address_object = UserAddress(user_address)

        # Compose the attributes object of user
        user_attributes = {
            'role': row['role'],
            'username': row['username'],
            'first_name': row['first_name'],
            'middle_name': row['middle_name'],
            'last_name': row['last_name'],
            'event_ids': events,
            'case_ids': cases,
            'email': row['email'],
            'phone': row['phone'],
            'address': user_address_object
        }
        user_attributes_object = UserAttribute(user_attributes)

        # Compose the data object of user
        user_data = {
            'id': row['user_id'],
            'type': user_resource_type,
            'links': {
                'self': uri_builder(f'{user_resource_type}/{row["user_id"]}')
            },
            'attributes': user_attributes_object
        }
        user_data_object = UserData(user_data)

        # Compose the top level object of JSON api for a user
        user_object = {
            'links': {
                'self': uri_builder(f'{user_resource_type}/{row["user_id"]}')
            },
            'data': user_data_object
        }
        user_response = UserTopLevel(user_object)

        # Serialize an object to native Python data types according to this
        # Schema's fields.
        user_response_json = UserSchema().dump(user_response)

        return user_response_json
