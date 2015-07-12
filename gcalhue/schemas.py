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


