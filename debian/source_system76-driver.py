"""
Apport package hook for system76-driver (requires Apport 2.5 or newer).

Copyright (C) 2005-2013 System76, Inc.
"""

from apport.hookutils import attach_file_if_exists

LOGS = (
    ('DriverLog', '/var/log/system76-driver.log'),
    ('DaemonLog', '/var/log/upstart/system76-driver.log'),
)


def add_info(report):
    report['CrashDB'] = "{'impl': 'launchpad', 'project': 'system76-driver'}"
    for (key, filename) in LOGS:
        attach_file_if_exists(report, filename, key)
