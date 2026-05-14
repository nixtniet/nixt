# This file is placed in the Public Domain.


"an object for a string"


import unittest


from nixt.face import Broker


class TestBroker(unittest.TestCase):

    def test_construct(self):
        broker = Broker()
        self.assertEqual(broker.objects, {})
