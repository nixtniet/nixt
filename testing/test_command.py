# This file is placed in the Public Domain.


"write your own commands"


import unittest


from nixt.defines import Commands, Message, Handler


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Commands()
        self.assertEqual(type(cmds), Commands)
