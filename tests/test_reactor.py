# This file is placed in the Public Domain.


"handler"


import unittest


from nixt.event   import Event
from nixt.modules import command
from nixt.run     import Reactor


hdl = Reactor()
hdl.register("command", command)
hdl.start()
hdl.raw = print


class TestReactor(unittest.TestCase):

    def test_loop(self):
        e = Event()
        e.txt = "dbg"
        hdl.put(e)
        e.wait()
        self.assertTrue(True)
