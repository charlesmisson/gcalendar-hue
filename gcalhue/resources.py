import yaml
from copy import copy
COLORS = {
        "clear": (1.,1.),
        "soon": (1.,1.),
        "now": (1.,1.),
}


class CalendarResource(object):
    def __init__(self, calendar, resource, bri=None, colors=None):
        self.calendar = calendar
        self.resource = resource
        self.uid_upcoming = None
        self.status = None
        self.change = False
        self.bri = max(1, min(bri or 128, 255))
        if colors:
            self.update_colors(colors)

    def alert(self, _type=None):
        _type = _type or "__default"
        pass

    def apply(self, state):
        # if self.change:
        #     self.alert()
        self.resource.on = True
        self.resource.xy = COLORS.get(state)

    def update_colors(self, colors):
        print self.calendar
        print self.bri
        for k, val in colors.items():
            print k, val
        print

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


class _DoesNotExist(object):
    pass

class YAMLPreferenceLoader(object):
    def __init__(self, _file):
        try:
            _f = yaml.load(
                _file.read())
            if type(_f) is str or not _f:
                raise TypeError
        except Exception, e:
            raise e
        self._data = _f

    def get(self, *args, **kwargs):
        # Named kwargs in py3 would fix this. :-/
        default = kwargs.get('default', _DoesNotExist())
        loc = self._data
        for k in args:
            loc = loc.get(k)
            if loc is None:
                if type(default) is _DoesNotExist:
                    raise ValueError
                else:
                    return default
        # if a dict is returned, it must be a copy so that any update methods
        # don't overwrite the data in-memory.
        return copy(loc)



