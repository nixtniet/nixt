# This file is placed in the Public Domain.


"engine"


import unittest


from nixt.encoder import dumps, loads
from nixt.objects import skip
from nixt.persist import Cache


default = {}


class TestPersist(unittest.TestCase):

    def test_cache(self):
        cache = Cache()
        self.assertEqual(type(cache), Cache)
