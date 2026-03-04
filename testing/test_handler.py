# This file is placed in the Public Domain.
# pylint: disable=C0103,C0115,C0116,W0105
# pylint: disable=W0212


"handler tests"


import unittest


from nixt.handler import Client, Console, Event, Handler, Output
from nixt.objects import values


buffer = []


class Message(Event):

    def __init__(self):
        super().__init__()
        self.kind = "hello"
        self.text = "hello"


class MyClient(Client):

    def raw(self, text):
        buffer.append(text)


class MyConsole(Console):

    def raw(self, text):
        buffer.append(text)


class MyOutput(Output):

    def raw(self, text):
        buffer.append(text)


def hello(event):
    event.reply(event.text)
    event.ready()


class TestHandler(unittest.TestCase):

    hdl = Handler()

    def setUp(self):
        self.hdl.register("hello", hello)
        self.hdl.start()

    def shutDown(self):
        self.hdl.stop()

    def test_callback(self):
        evt = Message()
        self.hdl.callback(evt)
        evt.wait()
        self.assertTrue("hello" in evt.result.values())

    def test_loop(self):
        evt = Message()
        self.hdl.put(evt)
        evt.wait()
        self.assertTrue(evt.isready.is_set())

    def test_put(self):
        hdl = Handler()
        evt = Message()
        hdl.put(evt)
        event = hdl.queue.get()
        self.assertTrue(event is evt)

    def test_register(self):
        self.hdl.register("hlo", hello)
        self.assertTrue(hello in self.hdl.cbs.values())

    def test_start(self):
        hdl = Handler()
        hdl.start()
        self.assertTrue(hdl.running.is_set())

    def test_stop(self):
        self.hdl.stop()
        self.assertTrue(not self.hdl.running.is_set())


class TestClient(unittest.TestCase):

    clt = MyClient()

    def setUp(self):
        self.clt.silent = False
        self.clt.register("hello", hello)
        self.clt.start()

    def shutDown(self):
        self.clt.stop()

    def test_announce(self):
        self.clt.announce("hello")
        self.assertTrue("hello" in buffer)

    def test_display(self):
        evt = Message()
        evt.reply("test1")
        evt.reply("test2")
        self.clt.display(evt)
        self.assertTrue("test1" in buffer)
        self.assertTrue("test2" in buffer)
        self.assertTrue(buffer.index("test1") < buffer.index("test2"))

    def test_dosay(self):
        self.clt.dosay("", "yo!")
        self.assertTrue("yo!" in buffer)

    def test_loop(self):
        evt = Message()
        self.clt.put(evt)
        evt.wait()
        self.assertTrue("hello" in evt.result.values())

    def test_poll(self):
        clt = Client()
        evt = Message()
        clt.iqueue.put(evt)
        event = clt.poll()
        self.assertTrue(event is evt)

    def test_put(self):
        evt = Message()
        self.clt.put(evt)
        evt.wait()
        self.assertTrue("hello" in values(evt.result))

    def test_raw(self):
        evt = Message()
        self.clt.put(evt)
        evt.wait()
        self.assertTrue("hello" in values(evt.result))


class TestConsole(unittest.TestCase):

    clt = MyConsole()

    def setUp(self):
        self.clt.silent = False
        self.clt.register("hello", hello)
        self.clt.start()

    def shutDown(self):
        self.clt.stop()

    def test_loop(self):
        evt = Message()
        self.clt.put(evt)
        evt.wait()
        self.assertTrue(evt.isready.is_set())

    def test_poll(self):
        clt = Console()
        evt = Message()
        clt.iqueue.put(evt)
        event = clt.poll()
        self.assertTrue(event is evt)


class TestOutput(unittest.TestCase):

    clt = MyOutput()

    def setUp(self):
        self.clt.silent = False
        self.clt.register("hello", hello)
        self.clt.start()

    def shutDown(self):
        self.clt.stop()

    def test_output(self):
        evt = Message()
        self.clt.put(evt)
        self.clt.oqueue.join()
        self.assertEqual(self.clt.oqueue.qsize(), 0)

    def test_start(self):
        self.assertTrue(self.clt.running.is_set())

    def test_stop(self):
        self.clt.stop()
        self.assertTrue(not self.clt.running.is_set())

    '''
    def test_wait(self):
        global buffer
        evt = Message()
        self.clt.put(evt)
        self.clt.wait()
        self.assertTrue("hello" in buffer)
    '''
