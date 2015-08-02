from .application_base import Application
from .resources import YAMLPreferenceLoader
import click
import logging
import sys
logging.basicConfig()
logger = logging.getLogger('gcal-hue')


@click.group()
def main():
    pass


def load_application(pref_file, interactive=False):
    try:
        preferences = YAMLPreferenceLoader(pref_file)
    except Exception, e:
        if interactive:
            print "Error loading Preferences"
        else:
            logger.error(repr(e))
        sys.exit(1)
    return preferences, Application(preferences, logger)


@main.command(help="Run application.")
@click.argument("pref", type=click.File())
def run(pref):
    preferences, app = load_application(pref)
    if app.log.isEnabledFor(logging.DEBUG):
        import pprint
        for l in pprint.pformat(preferences._data).split('\n'):
            logger.debug(">  "+l.strip())
    try:
        app.run()
    except KeyboardInterrupt:
        app.log.info("Shutting down on keyboard Interrupt")
        for cal in app.calendars:
            cal.resource.on = False


@main.command(help="List all calendars and their IDs")
@click.argument("pref", type=click.File())
def list(pref):
    preferences, app = load_application(pref, True)
    calendars = app.service.calendarList().list().execute()
    for c in calendars.get('items'):
        print "%s\n %s\n" % (c['summary'], c['id'])


if __name__ == '__main__':
    main()
