# This file is placed in the Public Domain.


"defines tests"


import unittest


from nixt.defines import StaticMethod


class Meta(StaticMethod):

    pass


class TestDefines(unittest.TestCase):

    def test_meta(self):
        meta = Meta()
        self.assertTrue(isinstance(meta, Meta))

    def test_static(self):
        sm = StaticMethod()
        self.assertTrue(isinstance(sm, StaticMethod))
