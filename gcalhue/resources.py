import phue

def get_hue(ip):
    return phue.Bridge(ip)


class CalendarResource(object):
    def __init__(self, calendar, resource):
        self.calendar = calendar
        self.resource = resource
        self.uid_upcoming = None
        self.status = None
        self.change = False

    def alert(self, _type=None):
        _type = _type or "__default"
        pass

    def apply(self, state):
        if self.change:
            self.alert()
        print self.calendar, state

    def change_for_status(self, events):
        if events[0][1]['iCalUID'] != self.uid_upcoming:
            self.uid_upcoming = events[0][1]['iCalUID']
            self.change = True

        first, second = [i[0] for i in events][:2]

        if first in ("clear", "soon",):
            self.apply(first)
        elif second == "soon":
            # First will always be "now" so either do a `soon` or a `now`
            # state for the viz.
            self.apply(second)
        else:
            self.apply(first)
        self.change = False
