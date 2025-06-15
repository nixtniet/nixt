# This file is placed in the Public Domain.


"handler"


import unittest


from nixt.event   import Event
from nixt.handler import Handler
from nixts        import command


hdl = Handler()
hdl.register("command", command)
hdl.start()


class TestHandler(unittest.TestCase):

    def test_loop(self):
        e = Event()
        e.txt = "dbg"
        hdl.put(e)
        e.wait()
        self.assertTrue(True)
