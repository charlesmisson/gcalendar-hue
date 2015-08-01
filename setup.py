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
          "click==4.0"
      ],
      entry_points="""
      [console_scripts]
      gcalhue=gcalhue:main
      """,
     )
