import httplib2
import os
import pprint
import datetime
import pdb

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = './secrets/google-sheets-client-secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def _get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    _credentials = store.get()
    if not _credentials or _credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            _credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            _credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return _credentials

def strip_cells(values):
  return [[cell.strip() for cell in row] for row in values]

def fetch_adventures(spreadsheetId):
  rangeName = 'adventures!A2:E'
  result = _service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=rangeName).execute()
  adventures = []
  values = strip_cells(result.get('values', []))
  if not values:
    return ('No adventures data', [])
  for i in range(len(values)):
    if len(values[i]) == 4:
      values[i].append(None)
    if len(values[i]) != 5:
      message = 'Bad row {}: {}'.format(i+1, pprint.pformat(values[i]))
      return (message, None)
  return (None, values)

def fetch_characters(spreadsheetId):
  rangeName = 'characters!A2:D'
  result = _service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=rangeName).execute()
  adventures = []
  values = strip_cells(result.get('values', []))
  if not values:
    return ('No characters data', [])
  for i in range(len(values)):
    if len(values[i]) == 3:
      values[i].append(None)
    if len(values[i]) != 4:
      message = 'Bad row {}: {}'.format(i+1, pprint.pformat(values[i]))
      return (message, None)
  return (None, values)

def fetch_data():
  spreadsheetId = '1sbTwpAv3zYglLGawRWADFXtSmLUihLcSPWbgc2ZuOQk'
  (message, adventures_result) = fetch_adventures(spreadsheetId)
  if not adventures_result:
    return (False, message, {})
  (message, characters_result) = fetch_characters(spreadsheetId)
  if not characters_result:
    return (False, message, {})

  # TODO fetch characters

  message = 'Fetched successfully.'
  return (True, message,
      {'adventures': adventures_result,
       'characters' : characters_result})

_credentials = _get_credentials()
_http = _credentials.authorize(httplib2.Http())
_discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
_service = discovery.build('sheets', 'v4', http=_http,
                           discoveryServiceUrl=_discoveryUrl)

def format_data(data):
  pass
