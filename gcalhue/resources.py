import yaml
from copy import copy
from schemas import PreferenceFile
COLORS = {
        "clear": (1.,1.),
        "soon": (1.,1.),
        "now": (1.,1.),
}


class CalendarResource(object):
    def __init__(self, calendar, resource, logger, bri=None, colors=None):
        self.calendar = calendar
        self.resource = resource
        self.uid_upcoming = None
        self.errors = False
        self.status = None
        self.change = False
        self.bri = max(1, min(bri or 128, 255))
        self.colors = colors or COLORS
        self.logger = logger

    def apply(self, state):
        color = self.colors.get(state, COLORS.get(state))
        self.logger.debug("Setting %s to %s" %(self.calendar, color))
        self.resource.on = True
        self.resource.brightness = self.bri
        self.resource.xy = color

    def change_for_status(self, events):
        # if events[0][1]['iCalUID'] == self.uid_upcoming:
        #     self.logger.debug("%s status is the same (%s)" % (
        #         self.calendar, events[0][0]
        #     ))
        #     return

        self.uid_upcoming = events[0][1]['iCalUID']
        first, second = [i[0] for i in events][:2]
        self.logger.debug("%s events: %s, %s" % (
                self.calendar, first, second
        ))
        if first in ("clear", "soon",):
            self.logger.info("%s changing to %s" % (self.calendar, first))
            self.apply(first)
        elif second == "soon":
            # First will always be "now" so either do a `soon` or a `now`
            # state for the viz.
            self.apply(second)
        else:
            self.apply(first)


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
        self._data, errors = PreferenceFile().load(_f)
        if errors:
            raise ValueError(repr(errors))

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



