from .application_base import Application
from .resources import YAMLPreferenceLoader
import click
import logging
import sys
logging.basicConfig()
logger = logging.getLogger('gcal-hue')


@click.command()
@click.argument("pref", type=click.File())
def main(pref):
    try:
        preferences = YAMLPreferenceLoader(pref)
    except:
        logger.error(" Misformatted or Empty Preference File")
        sys.exit(1)
    app = Application(preferences, logger)
    if app.log.isEnabledFor(logging.DEBUG):
        import pprint
        for l in pprint.pformat(preferences._data).split('\n'):
            logger.debug(l)
    #app.run()


if __name__ == '__main__':
    main()
