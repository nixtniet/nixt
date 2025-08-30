# This file is placed in the Public Domain.


"engine"


import unittest


from nixt.handler import Handler


class TestEngine(unittest.TestCase):

    def testcomposite(self):
        eng = Handler()
        self.assertEqual(type(eng), Handler)
