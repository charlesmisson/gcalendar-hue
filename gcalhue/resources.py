import yaml

COLORS = {
        "clear": (1.,1.),
        "soon": (1.,1.),
        "now": (1.,1.),
        "__default": (1.,1.)
}


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
        # if self.change:
        #     self.alert()
        self.resource.on = True
        self.resource.xy = COLORS.get(
            state,
            COLORS["__default"]
        )

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
        default = kwargs.get('default', False)
        loc = self._data
        for k in args:
            loc = loc.get(k)
            if loc is None:
                if default:
                    return default
                else:
                    raise ValueError
        return loc



