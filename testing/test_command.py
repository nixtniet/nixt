# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0415


"commands"


import unittest


from nixt.booting import cmds, cmnd, command
from nixt.handler import Client, Event
from nixt.objects import values


def cmd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_add(self):
        cmds.add(cmd)
        self.assertTrue(cmds.has("cmd"))

    def test_get(self):
        cmds.add(cmd)
        self.assertTrue(cmds.get("cmd"))

    def test_has(self):
        cmds.add(cmd)
        self.assertTrue(cmds.has("cmd"))

    def test_cmnd(self):
        cmds.add(cmd)
        self.assertTrue("yo!" in cmnd("cmd"))

    def test_scan(self):
        from testing import dbg
        cmds.scan(dbg)
        self.assertTrue("dbg" in cmds.cmds)

    def test_command(self):
        clt = Client()
        cmds.add(cmd)
        evt = Event()
        evt.text = "cmd"
        evt.orig = repr(clt)
        command(evt)
        self.assertTrue("yo!" in values(evt.result))
