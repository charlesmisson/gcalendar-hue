from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import httplib2
import datetime
import os
import logging
from time import sleep
import pytz
from schemas import Event_Schema


#  Standard colors for room states.
COLORS = {
    "clear": (1.,1.),
    "upcoming": (1.,1.),
    "booked": (1.,1.),
}


class Application(object):
    def __init__(self, calendars, interval=None, level=None):
        self.calendars = calendars
        self.interval = interval or 60 # one minute between checks.
        self.credentials = self.get_credentials()
        self.validator = Event_Schema()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)
        logging.basicConfig()
        self.log = logging.getLogger('gcal-hue')
        self.log.setLevel(level or logging.DEBUG)

    @staticmethod
    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        # Method is from google's quickstart.
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    @staticmethod
    def format_into_iso(date_object):
        return date_object.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    @staticmethod
    def now_utc_string():
        return datetime.datetime.utcnow().isoformat() + 'Z'

    @staticmethod
    def now():
        return datetime.datetime.now(pytz.utc)

    def unmarshall_event(self, event, strict=False):
        event, errors = self.validator.load(event)
        if strict and errors:
            raise ValueError(errors)
        return event

    def search_calendar(self, calendar, time=None, result_count=None):
        _results = result_count or 1
        if time:
            if type(time) is not str:
                _time = self.format_into_iso(time)
            else:
                _time = time
        else:
            _time = self.now_utc_string()
        return self.service.events().list(
            calendarId=calendar, timeMin=_time, maxResults=_results,
            singleEvents=True, orderBy="startTime"
        ).execute()


    def event_temporal_relation(self, event, time=None):
        """ Determine the relation of "now" to the top event.
        """
        characteristics = dict(soon=False, now=False)
        time = time or self.now()
        event_start = event['start']['dateTime']
        event_end
        pass

    def get_one_item(self, *args, **kwargs):
        # TODO:Transform into a generic getter for an accessor chain
        # get_one_item(['name', 0, 'name', 1]) ->
        #                                       _['name'][0]['name'][1]
        response = self.search_calendar(*args, **kwargs)
        return response.get('items', [None])[0]

    def run_task(self):
        for cal in self.calendars:
            print self.get_one_item(cal)

    def run(self):
        while True:
            self.run_task()
            sleep(self.interval)

