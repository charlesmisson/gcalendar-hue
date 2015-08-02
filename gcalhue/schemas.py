from marshmallow import Schema, fields

class _Date(Schema):
    dateTime = fields.DateTime()


class Event_Schema(Schema):
    status = fields.String()
    kind = fields.String()
    end = fields.Nested(_Date)
    description = fields.String()
    created = fields.DateTime()
    iCalUID = fields.String()
    reminders = fields.Field()
    htmlLink = fields.URL()
    sequence = fields.Integer()
    updated = fields.DateTime()
    summary = fields.String()
    start = fields.Nested(_Date)
    etag = fields.String()
    originalStartTime = fields.Nested(_Date)
    recurringEventId = fields.String()
    location = fields.String()
    attendees = fields.String()
    organizer = fields.Field()
    creator = fields.Field()
    id = fields.String()


class CalendarQuery(Schema):
    nextPageToken = fields.String()
    kind = fields.String()
    defaultReminders = fields.Field()
    # Main Body of the query.
    items = fields.List(fields.Nested(Event_Schema))
    updated = fields.DateTime()
    summary = fields.String()
    etag = fields.String()
    timeZone = fields.String()
    accessRole = fields.String()


class Calendar(Schema):
    calendar = fields.String(required=True)
    light = fields.String(required=True)
    suffix = fields.Boolean()
    bri = fields.Int()


class Colors(Schema):
    clear = fields.List(fields.Float(), missing=[.4,.2])
    soon = fields.List(fields.Float())
    now = fields.List(fields.Float())


class Hub(Schema):
    ip = fields.String(required=True)
    token = fields.String()


class GcalSettings(Schema):
    suffix = fields.String()
    light_maps = fields.List(fields.Nested(Calendar))

class Logging(Schema):
    enabled = fields.Boolean(default=True)
    level = fields.Int(default=20)

class PreferenceFile(Schema):
    google_calendar = fields.Nested(GcalSettings)
    soon = fields.Int(default=600)
    check_interval = fields.Int(default=10)
    philips_hue = fields.Nested(Hub)
    logging = fields.Nested(Logging)
    colors = fields.Nested(Colors)
