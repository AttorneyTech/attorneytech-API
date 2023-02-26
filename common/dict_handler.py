# Convert camel case to snake case
attributes_dict = {
    'users_attributes': {
       'firstName': 'first_name',
       'middleName': 'middle_name',
       'lastName': 'last_name',
       'email': 'email',
       'phone': 'phone',
       'addressLine1': 'street_name',
       'addressLine2': 'district',
       'zipCode': 'zip_code'
    }
}


def get_marshmallow_valid_message(data, values):
    '''
    Handling marshmallow ValidationError messages
    '''

    if isinstance(data, dict):
        for value in data.values():
            get_marshmallow_valid_message(value, values)
    else:
        values.append(data[0])

    return values


def get_patch_user_values(patch_attributes):
    '''
    Return set_columns and patch_values for patching user
    '''

    users_attributes = attributes_dict['users_attributes']
    set_columns = []
    patch_values = []

    def traverse_attributes(patch_attributes):
        for k, v in patch_attributes.items():
            if isinstance(v, dict):
                traverse_attributes(v)
            elif k in users_attributes and k not in ['caseIds', 'eventIds']:
                set_columns.append(f'{users_attributes[k]} = %s')
                patch_values.append(v)

    traverse_attributes(patch_attributes)
    return set_columns, patch_values
