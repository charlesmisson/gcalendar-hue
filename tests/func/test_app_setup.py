from gcalhue.application_base import Application
from ..base import TestBase
import pytest
import pytz
class TestSomething(TestBase):
    @pytest.fixture
    def app(self, secrets):
        calendars = secrets['calendars']
        return Application(calendars)

    def test_application(self, app):
        item = app.search_calendar(app.calendars[0],)

    def test_config(self, secrets):
        assert(secrets)

    def test_event_stability(self, secrets, app):
        """Make sure that an event currently underway is still the top thing
        found"""
        cname = secrets['calendars'][0]
        item = app.events(cname)[0]
        start = item['start']['dateTime']
        update = start.replace(minute=start.minute + 1, )
        #isostring = update.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        min_later = app.events(cname, time=update)[0]
        # Test is probably self evident...
        assert(update > item['start']['dateTime'])
        assert(min_later['iCalUID'] == item['iCalUID'])

    def test_report_inprogress(self, secrets, app):
        cname = secrets['calendars'][0]
        item = app.events(cname)[0]
        time = item['start']['dateTime']
        time = time.replace(minute=time.minute + 1,)
        assert(app.event_temporal_relation(item, time) == "now")

    def test_report_soon(self, secrets, app):
        cname = secrets['calendars'][0]
        item = app.events(cname)[0]
        time = item['start']['dateTime']
        time = time.replace(minute=time.minute - 1,)
        assert(app.event_temporal_relation(item, time) == "soon")

    def test_report_clear(self, secrets, app):
        cname = secrets['calendars'][0]
        item = app.events(cname)[0]
        time = item['start']['dateTime']
        time = time.replace(hour=time.hour - 1,)
        assert(app.event_temporal_relation(item, time) == "clear")

