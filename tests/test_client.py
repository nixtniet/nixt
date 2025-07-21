# This file is placed in the Public Domain.


"client"


import unittest


from nixt.client import Client


class TestClient(unittest.TestCase):

    def test_construct(self):
        clt = Client()
        self.assertEqual(type(clt), Client)
