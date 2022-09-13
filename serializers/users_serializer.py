from common.uri_builder import uri_builder
from schemas.users_schema import UserSchema, UsersSchema


# Type of user resource
user_resource_type = 'users'


class UserAddress:
    '''Construct address object of a user'''
    def __init__(self, user_address):
        self.addressLine1 = user_address['address_line_1']
        self.addressLine2 = user_address['address_line_2']
        self.city = user_address['city']
        self.zipCode = user_address['zip_code']


class UserAttribute:
    '''Construct attributes object of a user'''
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
    '''Construct data object of a user'''
    def __init__(self, user_data):
        self.id = user_data['id']
        self.type = user_data['type']
        self.links = user_data['links']
        self.attributes = user_data['attributes']


class UserTopLevel:
    '''Construct top level object of a user in JSON:API format'''
    def __init__(self, user_object):
        self.links = user_object['links']
        self.data = user_object['data']


class UsersSerializer:
    '''
    Combine with the objects of users and construct the serializer for users
    resource:
    Depending on whether it is get /users or get /users/{userId}, if it is
    the latter, call `raw_user_serializer()` and `user_response()` directly.
    If the former, the database will return data in list of dict format.
    Here generate a list of user id first, and according to this list, find
    the same user id and append to raw_users_list. And for each raw_users_list,
    pass it into `raw_user_serializer()` func, and append the object returned
    to user_data_object_list. Finally, return the user_data_object_list and
    call `users_response()`.
    '''
    @staticmethod
    def raw_users_serializer(raw_users):
        '''
        Variables:
        users_id_list -- list of users id which returns from database.
        raw_users_list -- a group of rows user data to pass as parameters
        into raw_user_serializer func.
        users_data_object_list -- list of users data objects which are
        returned from raw_user_serializer func.
        '''
        users_id_set = set()
        for row in raw_users:
            users_id_set.add(row['user_id'])
        users_id_list = list(users_id_set)
        users_id_list.sort()

        users_data_object_list = []
        for user_id in users_id_list:
            raw_users_list = []
            for row in raw_users:
                if row['user_id'] == user_id:
                    raw_users_list.append(row)
            users_data_object_list.append(
                UsersSerializer.raw_user_serializer(
                    raw_users_list
                )
            )
        return users_data_object_list

    @staticmethod
    def raw_user_serializer(raw_user):
        '''Serializes raw user data from user resource'''
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
        user_address = {
            'address_line_1': row['street_name'],
            'address_line_2': row['district'],
            'city': row['city'],
            'zip_code': row['zip_code']
        }
        user_address_object = UserAddress(user_address)
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
        user_data = {
            'id': row['user_id'],
            'type': user_resource_type,
            'links': {
                'self': uri_builder(f'{user_resource_type}/{row["user_id"]}')
            },
            'attributes': user_attributes_object
        }
        user_data_object = UserData(user_data)

        return user_data_object

    @staticmethod
    def user_response(user_data_object):
        '''Compose the top level object of JSON api for a user'''
        user_object = {
            'links': {
                'self': uri_builder(
                    f'{user_resource_type}/{user_data_object.id}'
                )
            },
            'data': user_data_object
        }
        user_response = UserTopLevel(user_object)
        user_response_json = UserSchema().dump(user_response)

        return user_response_json

    @staticmethod
    def users_response(user_attributes_object_list):
        '''Compose the top level object of JSON api for a users'''
        users_object = {
            'links': {
                'self': uri_builder(f'{user_resource_type}')
            },
            'data': user_attributes_object_list
        }
        user_response = UserTopLevel(users_object)
        users_response_json = UsersSchema().dump(user_response)

        return users_response_json
