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
        item = app.get_one_item(app.calendars[0],)
        event = app.unmarshall_event(item)['start']['dateTime']

    def test_config(self, secrets):
        assert(secrets)

    def test_event_stability(self, secrets, app):
        """Make sure that an event currently underway is still the top thing
        found"""
        cname = secrets['calendars'][0]
        item = app.unmarshall_event(app.get_one_item(cname))
        start = item['start']['dateTime']
        update = start.replace(minute=start.minute + 1, )
        #isostring = update.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        min_later = app.unmarshall_event(app.get_one_item(cname,
                                                          time=update))
        assert(update > item['start']['dateTime'])
        assert(min_later['summary'] == item['summary'])

    def test_x(self, app):
        x = app.search_calendar(app.calendars[0], result_count=1)
        for i in x:
            print i, x[i]

