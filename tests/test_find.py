# This file is placed in the Public Domain.


"find"


import unittest


from nixt.cache  import write
from nixt.find   import find
from nixt.object import Object
from nixt.paths  import ident


class TestFind(unittest.TestCase):

    def test_find(self):
        obj = Object()
        write(obj, ident(obj))
        result = list(find("nixt.object.Object"))
        self.assertNotEqual(len(result), 0)
