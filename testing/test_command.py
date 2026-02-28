# This file is placed in the Public Domain.


"commands"


import unittest


from nixt.command import commands, command
from nixt.handler import Client
from nixt.message import Message
from nixt.objects import values


def cmnd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_add(self):
        commands.add(cmnd)
        self.assertTrue(commands.has("cmnd"))
    
    def test_get(self):
        commands.add(cmnd)
        self.assertTrue(commands.get("cmnd"))

    def test_has(self):
        commands.add(cmnd)
        self.assertTrue(commands.get("cmnd"))
    
    def test_command(self):
        clt = Client()
        commands.add(cmnd)
        evt = Message()
        evt.text = "cmnd"
        evt.orig = repr(clt)
        command(evt)
        self.assertTrue("yo!" in values(evt.result))
