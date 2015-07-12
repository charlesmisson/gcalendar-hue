from .application_base import Application

calendars = []


def main():
    app = Application(calendars)
    app.run()


if __name__ == '__main__':
    main()
