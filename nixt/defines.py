# This file is placed in the Public Domain.


"defines"


import logging


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning':logging. WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


SYSTEMD = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


TIMES = [
    "%Y-%M-%D %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d"
]


def __dir__():
    return (
        'LEVELS',
        'SYSTEMD',
        'TIMES'
    )
