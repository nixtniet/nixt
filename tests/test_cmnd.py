# This file is placed in the Public Domain.


"command"


import unittest


from nixt.cmnd import Commands


class TestCommand(unittest.TestCase):

    def test_construct(self):
        cmd = Commands()
        self.assertEqual(type(cmd), Commands)
