# This file is placed in the Public Domain.


"path tests"


import unittest


from nixt.paths import Workdir, setwd


class TestComposite(unittest.TestCase):

    def test_setwd(self):
        setwd("bla", "bla")
        self.assertEqual(Workdir.wdr, "bla")
