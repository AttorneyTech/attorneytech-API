import json
import sys
import traceback


# Open the config file and validate it with config-example
try:
    with open('config.json', 'r') as config_f:
        config = json.load(config_f)
    with open('config-example.json', 'r') as config_f_ex:
        config_ex = json.load(config_f_ex)
except Exception:
    traceback.print_exc()
    sys.exit()


# Validate the top-level keys in config file.
# If the top-level keys in config file is different from example config file,
# append it into list of diff_keys or keep checking the sub-level keys.
diff_keys = []
top_keys_diff = set(config_ex).difference(set(config))

if top_keys_diff:
    diff_keys.append(top_keys_diff)
else:
    for key in config.keys():
        for key_ex in config_ex.keys():
            if key == key_ex:
                sub_keys_diff = (
                    set(config_ex[key_ex]).difference(set(config[key]))
                )
                if sub_keys_diff:
                    diff_keys.append({key: sub_keys_diff})

# If any keys is setting wrong or missing, raise an error
# and show the keys which just caught in diff_keys.
if diff_keys:
    raise KeyError(
        f'These key in your config file may be wrong or missing: {diff_keys}'
    )

config_server = config['server']
config_auth = config['authentication']
config_db = config['database']
config_logger = config['logger']
