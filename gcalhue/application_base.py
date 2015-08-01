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
from resources import CalendarResource
import phue



class Application(object):
    def __init__(self, prefs, logger):
        self.prefs = prefs
        if prefs.get('logging', 'enabled', default=False):
            self.log = logger
            self.log.setLevel(prefs.get('logging', 'level', default=20))
        self.soon = prefs.get('soon', default=600)
        self.interval = prefs.get('check_interval', default=60)
        self.credentials = self.get_credentials()
        self.validator = CalendarQuery()
        self.suffix = prefs.get('google_calendar', 'suffix', default=None)

        # self.http = self.credentials.authorize(httplib2.Http())
        # self.service = discovery.build('calendar', 'v3', http=self.http)
        self.hue = phue.Bridge(prefs.get('philips_hue', 'ip'))
        # The Phue library is finicky, won't load lights until invoked
        self.lights = self.hue.lights_by_name
        self.log.debug(" ".join(l.name for l in self.hue.lights))

        self.calendars = self._build_calendars(
            self.prefs.get('google_calendar', default={}))
    def light_for_name(self, name):
        return self.lights.get(name, None)

    def _suffix_string(self, _dict, accessor="calendar"):
        _dict[accessor] = _dict.pop(accessor) + self.suffix
        return _dict

    def _build_one_cal(self, settings):
        cal = settings['calendar']
        light = self.light_for_name(
            settings['light'])
        return CalendarResource(cal, light)

    def _build_calendars(self, cal_settings):
        cals = cal_settings.get('light_maps', [])
        if self.suffix:
            cals = map(self._suffix_string, cals)
        return map(self._build_one_cal, cals)

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

    def error_and_exit(self, error):
        self.log.error(repr(error))
        sys.exit(1)

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
            self.error_and_exit("No Calendars")
        for cal in self.calendars:
            events = self.events(cal.calendar)
            if events:
                relations = map(self.event_temporal_relation, events)
                cal.change_for_status(relations)

    def run(self):
        if not self.calendars:
            self.error_and_exit("No Calendars Found")
        while True:
            self.run_task()
            sleep(self.interval)

