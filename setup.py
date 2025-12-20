#!/usr/bin/env python3


"stub"


import setuptools


setuptools.setup(
    data_files=[
        ('share/nixt/examples', [
            'examples/__init__.py',
            'examples/atr.py',
            'examples/flt.py',
            'examples/fnd.py',
            'examples/irc.py',
            'examples/log.py',
            'examples/lst.py',
            'examples/mbx.py',
            'examples/mdl.py',
            'examples/pth.py',
            'examples/req.py',
            'examples/rss.py',
            'examples/rst.py',
            'examples/sil.py',
            'examples/slg.py',
            'examples/tdo.py',
            'examples/thr.py',
            'examples/tmr.py',
            'examples/udp.py',
            'examples/upt.py',
            'examples/web.py',
            'examples/wsd.py'
            ]
        )
    ],
    scripts=[
        "bin/nixt",
    ])
