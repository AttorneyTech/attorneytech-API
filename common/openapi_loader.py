import sys
import traceback

from yaml import load, Loader


def safe_get(_dict: dict, *keys: str):
    '''
    Safe get the value of nested dict
    '''

    for key in keys:
        try:
            _dict = _dict[key]
        except KeyError:
            return None
    return _dict


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

filter_enums = {
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
resources_type = {
    'users': safe_get(schemas, 'UserType', 'enum')[0],
    'events': safe_get(schemas, 'EventType', 'enum')[0],
    'cases': safe_get(schemas, 'CaseType', 'enum')[0],
    'court': safe_get(schemas, 'CourtType', 'enum')[0],
    'section_in_charge': safe_get(schemas, 'SectionInChargeType', 'enum')[0],
    'opposite_client': safe_get(schemas, 'OppositeClientType', 'enum')[0],
    'opposite_agent': safe_get(schemas, 'OppositeAgentType', 'enum')[0],
    'paper_type': safe_get(schemas, 'PaperType', 'enum')[0],
    'paper_file_type': safe_get(schemas, 'PaperFileType', 'enum')[0]
}
