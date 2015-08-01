from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import httplib2
import datetime
import os
import logging
import sys
from time import sleep
import pytz
from schemas import CalendarQuery
import phue
from resource import CalendarResource

logging.basicConfig()

#  Standard colors for room states.
COLORS = {
    "clear": (1.,1.),
    "soon": (1.,1.),
    "now": (1.,1.),
    "__default": (1.,1.)
}


class Application(object):
    def __init__(self, calendars, interval=None, level=None):
        self.calendars = calendars
        self.soon = 600
        self.interval = interval or 60 # one minute between checks.
        self.credentials = self.get_credentials()
        self.validator = CalendarQuery()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)
        self.log = logging.getLogger('gcal-hue')
        self.log.setLevel(level or logging.DEBUG)

    def __build_calendars(self, calendars):
        return map(
            lambda cal: CalendarResource(cal, 0),
            calendars)

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
    def nows():
        return datetime.datetime.utcnow().isoformat() + 'Z'

    @staticmethod
    def now():
        return datetime.datetime.now(pytz.utc)

    def search_calendar(self, calendar, time=None,
                        result_count=None, strict=False):
        _results = result_count or 2
        if time and type(time) is not str:
            _time = self.format_into_iso(time)
        else:
            _time = time or self.nows()

        query, errors = self.validator.load(self.service.events().list(
            calendarId=calendar, timeMin=_time, maxResults=_results,
            singleEvents=True, orderBy="startTime"
        ).execute())

        if errors and strict:
            raise ValueError(errors)
        return query

    def events(self, *args, **kwargs):
        return self.search_calendar(*args, **kwargs).get('items', [])

    def event_temporal_relation(self, event, time=None):
        """ Determine the relation of "now" to the top event.
        """
        time = time or self.now()
        event_start = event['start']['dateTime']
        event_end = event['end']['dateTime']
        if event_start < time < event_end:
            return "now", event
        if event_start > time and (event_start - time).seconds <= self.soon:
            return "soon", event
        return "clear", event

    def map_relations(self, events, time=None):
        return map(lambda x: self.event_temporal_relation(x, time), events)

    def run_task(self):
        if not self.calendars:
            print "No Calendars Found"
            sys.exit(1)
        for cal in self.calendars:
            events = self.events(cal.calendar)
            if events:
                relations = map(self.event_temporal_relation, events)
                cal.change_for_status(relations)

    def run(self):
        while True:
            self.run_task()
            sleep(self.interval)

