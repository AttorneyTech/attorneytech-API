import sys
import traceback

from yaml import load, Loader


def safe_get(openapi_dict: dict, *keys: str):
    '''
    Safe get the value of nested dict from openapi.yaml
    '''

    for key in keys:
        try:
            openapi_dict = openapi_dict[key]
        except KeyError:
            traceback.print_exc()
            sys.exit()
    return openapi_dict


# Load the openapi.yaml file and read the content as a dict
try:
    with open('openapi.yaml', 'r') as f:
        openapi_spec = load(f, Loader=Loader)
except Exception:
    traceback.print_exc()
    sys.exit()

# Reusable dicts
components = safe_get(openapi_spec, 'components')
schemas = safe_get(components, 'schemas')
user_attributes = safe_get(schemas, 'UserAttributes')

# Enums
enums = {
    'users': {
        'filter[role]': safe_get(
            user_attributes,
            'properties', 'role', 'enum'
        ),
        'filter[city]': safe_get(
            user_attributes,
            'properties', 'address', 'properties', 'city', 'enum'
        )
    }
}

# Resource type of resource objects which defined in JSON API
resources_type = {}

for k, v in schemas.items():
    if 'Type' in k:
        resources_type[v.get('enum')[0]] = v.get('enum')[0]
