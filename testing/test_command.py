# This file is placed in the Public Domain.


"write your own commands"


import unittest


from nixt.defines import Engine, Message, Mods


def cmnd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Mods()
        self.assertEqual(type(cmds), Mods)

    def test_add(self):
        Mods.add(cmnd)
        self.assertTrue("cmnd" in Mods.cmds)

    def test_get(self):
        Mods.add(cmnd)
        self.assertTrue(Mods.cmds.get("cmnd"))

    def test_command(self):
        clt = Engine()
        Mods.add(cmnd)
        evt = Message()
        evt.text = "cmnd"
        evt.orig = repr(clt)
        Mods.command(evt)
        self.assertTrue("yo!" in evt.result)
