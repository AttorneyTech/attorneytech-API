import json
import sys
import traceback


try:
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)
except Exception:
    traceback.print_exc()
    sys.exit()
