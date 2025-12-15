# This file is placed in the Public Domain.


"methods"


import unittest


from nixt.classes import Method, Object


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Object()
        o.a = "b"
        self.assertEqual(Method.fmt(o), 'a="b"')
