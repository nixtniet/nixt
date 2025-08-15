# This file is placed in the Public Domain.


"path tests"


import unittest


from nixt.modules import Workdir, setwd


class TestComposite(unittest.TestCase):

    def test_setwd(self):
        setwd("nixt", ".test")
        self.assertEqual(Workdir.wdr, ".test")
