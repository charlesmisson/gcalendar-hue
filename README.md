# gcalendar-hue
Google Calendar resource statuses rendered to Philips Hue bulbs. This application takes a configuration file which checks individual google calendars for a free/busy/soon-to-be-busy status, then uses that command to change the color of a light.

## Prerequisites

- Project with Google Calendar API access set up in Google Console
- client_secrets.json downloaded to computer.


## Overview
The command can be invoked with:

```$ gcalhue /path/to/config.yaml```

## Options
```
google_calendar:
  suffix: "@resource.calendar.google.com"
  light_maps:
    - calendar: fakecalendar_40923840923840
      light: Splash Wall
    - calendar: myemail@gmail.com
      suffix: False
      light: Ambient Computer
      bri: 128
soon: 600
check_interval: 10
philips_hue:
  ip: 192.168.0.19
  token: aef51bb819bfd4ee9f3391f82183357
logging:
  enabled: true
  level: 20
colors:
  clear: [0.3922, 0.4842]
  soon: [0.5594, 0.4008]
  now: [0.6713, 0.3234]
```
