# This file is placed in the Public Domain.


"interface"


import unittest


import nixt.defines as dev


interface = (
       'Boot',
       'Broker',
       'Buffer',
       'Buffered',
       'Client',
       'Clients',
       'Cmd',
       'Commands',
       'Disk',
       'Engine',
       'Json',
       'Locate',
       'Logging',
       'Main',
       'Md5',
       'Message',
       'Mods',
       'Method',
       'Object',
       'Output',
       'Parse',
       'Repeater',
       'Task',
       'Thread',
       'Time',
       'Utils',
       'Workdir'
    )


class TestDefines(unittest.TestCase):

    def test_dir(self):
        self.assertTrue(len(dir(dev)), 22)

    def test_interface(self):
        self.assertTrue(dir(dev), interface)
