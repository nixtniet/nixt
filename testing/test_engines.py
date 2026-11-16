# This file is placed in the Public Domain.


"pool"


import unittest


from nixt.engines import Engine


class TestEngine(unittest.TestCase):

    "pool unittests"

    def test_construct(self):
        "test pool construction."
        engine = Engine()
        self.assertTrue(type(engine), Engine)
