import json
import argparse
import sys
import requests

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--organization', type=str, default='kagarlickij')
PARSER.add_argument('--projectName', type=str)
PARSER.add_argument('--pat', type=str)

ARGS = PARSER.parse_args()

if not ARGS.projectName or not ARGS.pat:
    print(f'[ERROR] missing required arguments')
    sys.exit(1)

print(f'[INFO] Deleting tmp Release pipeline..')
URL = 'https://vsrm.dev.azure.com/{}/{}/_apis/release/definitions/1?api-version=5.0'.format(ARGS.organization, ARGS.projectName)
HEADERS = {
    'Content-Type': 'application/json',
}

try:
    RESPONSE = requests.delete(URL, headers=HEADERS, auth=(ARGS.pat,''))
    RESPONSE.raise_for_status()
except Exception as err:
    print(f'[ERROR] {err}')
    RESPONSE_TEXT = json.loads(RESPONSE.text)
    CODE = RESPONSE_TEXT['errorCode']
    MESSAGE = RESPONSE_TEXT['message']
    print(f'[ERROR] Response code: {CODE}')
    print(f'[ERROR] Response message: {MESSAGE}')
    sys.exit(1)
else:
    RESPONSE_CODE = RESPONSE.status_code
    if RESPONSE_CODE == 204:
        print(f'[INFO] tmp Release pipeline has been deleted successfully')
    else:
        print(f'[ERROR] tmp Release pipeline has not been deleted')
        sys.exit(1)
