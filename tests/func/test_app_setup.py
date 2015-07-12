from gcalhue.application_base import Application
from ..base import TestBase
import pytest

class TestSomething(TestBase):
    @pytest.fixture
    def app(self, secrets):
        calendars = secrets['calendars']
        return Application(calendars)

    def test_application(self, app):
        item = app.get_one_item(app.calendars[0],
                                time="2015-07-14T22:10:00.435944Z")
        now = app.now()
        event = app.unmarshall_event(item)['start']['dateTime']
        print now, event
        print now.tzinfo
        print event > now

    def test_config(self, secrets):
        print secrets or "None"
