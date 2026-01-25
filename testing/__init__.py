# This file is placed in the Public Domain.
# ruff: noqa: F403,F405


"interface"


import logging
import os
import sys
import unittest


sys.path.insert(0, os.getcwd())


import nixt
import nixt.brokers
import nixt.command
import nixt.encoder
import nixt.handler
import nixt.message
import nixt.methods
import nixt.objects
import nixt.package
import nixt.persist
import nixt.runtime
import nixt.threads
import nixt.utility


TARGET = nixt


PACKAGE = [
    'brokers',
    'command',
    'encoder',
    'handler',
    'message',
    'methods',
    'objects',
    'package',
    'persist',
    'runtime',
    'threads',
    'utility'
]


class TestInterface(unittest.TestCase):

    def test_package(self):
        okd = True
        for mod in PACKAGE:
            mod1 = getattr(TARGET, mod, None)
            if not mod1:
                okd = False
                print(mod)
                break
        self.assertTrue(okd)
