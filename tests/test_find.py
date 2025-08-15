# This file is placed in the Public Domain.


"find tests"


import unittest


from nixt.modules import find, setwd


setwd('.test')


class TestFind(unittest.TestCase):

    def test_find(self):
        res = list(find('log'))
        self.assertEqual(res, [])
