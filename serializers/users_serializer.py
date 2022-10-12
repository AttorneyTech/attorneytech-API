import urllib.parse

from flask import request

from common.openapi_loader import resources_type
from common.uri_builder import uri_builder
from schemas.users_schema import UserSchema, UsersSchema


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
    resource.
    '''

    @staticmethod
    def raw_users_serializer(raw_users):
        '''
        The database will return data in list of dict RealDictRow format.
        Call the `raw_users_serializer()` function and pass each raw_user data
        into `raw_user_serializer()` by iterating over raw_users and get the
        users_objects list. Finally call the `users_response()` function.
        '''

        users_objects = []
        users_collection = {}
        for raw_user in raw_users:
            if raw_user['user_id'] not in users_collection:
                users_collection[raw_user['user_id']] = [raw_user]
            else:
                users_collection[raw_user['user_id']].append(raw_user)

        for raw_user in users_collection.values():
            users_objects.append(UsersSerializer.raw_user_serializer(raw_user))
        return users_objects

    @staticmethod
    def raw_user_serializer(raw_user):
        '''Serializes raw user data from user resource.'''

        event_ids, case_ids = [], []
        # Serialize the `event_ids` and `case_ids`
        # And since the different cases could be the same event, here
        # needs to handle the duplicate event_id.
        for row in raw_user:
            if row['event_id'] not in event_ids:
                event_ids.append(row['event_id'])
            case_ids.append(row['case_id'])

        # Since the RealDictCursor return the list of RealDictRow object,
        # here assign the single object to raw_user to serialize the rest
        # part of user data.
        raw_user = raw_user[0]
        user_address = {
            'address_line_1': raw_user['street_name'],
            'address_line_2': raw_user['district'],
            'city': raw_user['city'],
            'zip_code': raw_user['zip_code']
        }
        user_address_object = UserAddress(user_address)
        user_attributes = {
            'role': raw_user['role'],
            'username': raw_user['username'],
            'first_name': raw_user['first_name'],
            'middle_name': raw_user['middle_name'],
            'last_name': raw_user['last_name'],
            'event_ids': event_ids,
            'case_ids': case_ids,
            'email': raw_user['email'],
            'phone': raw_user['phone'],
            'address': user_address_object
        }
        user_attributes_object = UserAttribute(user_attributes)
        user_data = {
            'id': raw_user['user_id'],
            'type': resources_type['users'],
            'links': {
                'self': uri_builder(
                    f'{resources_type["users"]}/{raw_user["user_id"]}'
                )
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
                    f'{resources_type["users"]}/{user_data_object.id}'
                )
            },
            'data': user_data_object
        }
        user_response = UserTopLevel(user_object)
        schema = UserSchema()
        serialized_user = schema.dump(user_response)
        return serialized_user

    @staticmethod
    def users_response(user_attributes_object_list):
        '''Compose the top level object of JSON api for a users'''

        uri = request.url
        uri = urllib.parse.unquote(uri)
        users_object = {
            'links': {
                'self': uri
            },
            'data': user_attributes_object_list
        }
        user_response = UserTopLevel(users_object)
        schema = UsersSchema()
        serialized_users = schema.dump(user_response)
        return serialized_users
