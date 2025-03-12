# This file is placed in the Public Domain.


"handler"


import unittest


from nixt.cmnd    import command
from nixt.reactor import Event, Handler


hdl = Handler()
hdl.register("command", command)
hdl.start()
hdl.raw = print


class TestHandler(unittest.TestCase):

    def test_loop(self):
        e = Event()
        e.txt = "dbg"
        hdl.put(e)
        e.wait()
        self.assertTrue(True)

