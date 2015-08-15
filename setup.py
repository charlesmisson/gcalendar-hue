#!/usr/bin/env python

from distutils.core import setup

setup(name='gcal-hue',
      version='0.01',
      description='Calendar Monitoring for Hue bulbs',
      author='Nate Swanson',
      author_email='swanson.nate@gmail.com',
      packages=['gcalhue'],
      py_modules=['scripts/bonusly'],
      install_requires=[
          "PyYAML==3.11",
          "click==4.0",
          "marshmallow",
          "pytz",
          "google-api-python-client==1.4.1",
          "phue==0.8"
      ],
      entry_points="""
      [console_scripts]
      gcalhue=gcalhue:main
      """,
     )
