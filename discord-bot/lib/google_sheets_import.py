import httplib2
import os
import pprint
import datetime
import pdb

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from lib import in_game_calendar
from lib import adventure

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

def fetch_adventures(spreadsheetId):
  rangeName = 'adventures!A2:E'
  result = _service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=rangeName).execute()
  adventures = []
  values = result.get('values', [])
  for i in range(len(values)):
    row = values[i]
    if len(row) not in (4, 5):
      message = 'Bad row {}: {}'.format(i+1, pprint.pformat(row))
      return (message, None)
    if len(row) == 4:
      row.append('')
    this_adventure = adventure.Adventure(
        name=row[0],
        start_date=in_game_calendar.InGameDate.FromString(row[1]),
        end_date=in_game_calendar.InGameDate.FromString(row[2]),
        real_date=datetime.datetime.strptime(row[3], '%Y-%m-%d').date())
    adventures.append(this_adventure)
  return (None, adventures)

def fetch_data():
  spreadsheetId = '1sbTwpAv3zYglLGawRWADFXtSmLUihLcSPWbgc2ZuOQk'
  (message, adventures_result) = fetch_adventures(spreadsheetId)
  if not adventures_result:
    return (False, message, {})

  message = 'Fetched successfully.'
  return (True, message, {'adventures': adventures_result})

_credentials = _get_credentials()
_http = _credentials.authorize(httplib2.Http())
_discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
_service = discovery.build('sheets', 'v4', http=_http,
                           discoveryServiceUrl=_discoveryUrl)

def format_data(data):
  pass
