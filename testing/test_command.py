# This file is placed in the Public Domain.


"commands"


import unittest


from nixt.brokers import Broker
from nixt.command import Commands
from nixt.handler import Client
from nixt.message import Message
from nixt.methods import parse
from nixt.objects import values


broker = Broker()
cmds = Commands()


def cmd(event):
    event.reply("yo!")


def cmnd(text):
    "parse text for command and run it."
    results = {}
    for txt in text.split(" ! "):
        evt = Message()
        evt.text = txt
        evt.type = "command"
        command(evt)
        evt.wait()
        results.update(evt.result)
    return results.values()


def command(evt):
    "command callback."
    parse(evt, evt.text)
    func = cmds.get(evt.cmd)
    if func:
        func(evt)
        bot = broker.retrieve(evt.orig)
        if bot:
            bot.display(evt)
    evt.ready()


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
        import testing.dbg as dbg
        cmds.scan(dbg)
        self.assertTrue("dbg" in cmds.cmds)

    def test_command(self):
        clt = Client()
        cmds.add(cmd)
        evt = Message()
        evt.text = "cmd"
        evt.orig = repr(clt)
        command(evt)
        self.assertTrue("yo!" in values(evt.result))
