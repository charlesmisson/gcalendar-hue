import yaml
from copy import copy
from schemas import PreferenceFile
COLORS = {
        "clear": (1.,1.),
        "soon": (1.,1.),
        "now": (1.,1.),
}


class CalendarResource(object):
    def __init__(self, calendar, resource, logger,
                 name=None, bri=None, colors=None):
        self.calendar = calendar
        self.resource = resource
        self.name_for_people = name
        self.trigger_uid = None
        self.errors = False
        self.status = None
        self.change = False
        self.bri = max(1, min(bri or 128, 255))
        self.colors = colors or COLORS
        self.logger = logger

    def apply(self, state):
        color = self.colors.get(state, COLORS.get(state))
        self.logger.info("%s is %s, setting to %s with %s light" %(
            self.name_for_people, state, color, self.resource.name
        ))
        self.resource.on = True
        self.resource.brightness = self.bri
        self.resource.xy = color

    def trigger(self, state, uid):
        if uid == self.trigger_uid:
            return
        self.logger.debug("Event JSON Hash changed.")
        self.trigger_uid = uid
        self.apply(state)

    def change_for_status(self, events):
        self.uid_upcoming = events[0][1]['iCalUID']
        first, second = [i[0] for i in events][:2]
        f_uid, s_uid = [hash(str(i[1])) for i in events][:2]
        self.logger.debug("%s events: %s, %s" % (
                self.name_for_people, first, second
        ))
        if second == "soon":
            self.trigger(second, s_uid)
        else:
            self.trigger(first, f_uid)

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



