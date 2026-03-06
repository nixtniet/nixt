# This file is placed in the Public Domain.


"commands"


import unittest


from nixt.handler import Client, Message
from nixt.command import Commands
from nixt.objects import Dict


def cmnd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Commands()
        self.assertEqual(type(cmds), Commands)

    def test_add(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.has("cmnd"))

    def test_get(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.get("cmnd"))

    def test_has(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.get("cmnd"))

    def test_command(self):
        clt = Client()
        Commands.add(cmnd)
        evt = Message()
        evt.text = "cmnd"
        evt.orig = repr(clt)
        Commands.command(evt)
        self.assertTrue("yo!" in Dict.values(evt.result))
