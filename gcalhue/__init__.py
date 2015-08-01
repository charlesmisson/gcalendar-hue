from .application_base import Application

calendars = [
    "calendar@resource.calendar.google.com",
]


def main():
    app = Application(calendars)
    app.run()


if __name__ == '__main__':
    main()
