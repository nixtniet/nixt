# This file is placed in the Public Domain.


"utilities"


import time
import unittest


from nixt.defines import Time, Utils


class TestTime(unittest.TestCase):

    def test_construct(self):
        tme = Time()
        self.assertTrue(tme)

    def test_date(self):
        pass

    def test_elapsed(self):
        pass

    def test_extract(self):
        pass

    def test_fntime(self):
        pass

    def test_timed(self):
        pass

    def test_today(self):
        pass


class TestUtils(unittest.TestCase):

    def test_cdir(self):
        pass

    def test_check(self):
        pass

    def test_clsname(self):
        pass

    def test_listdir(self):
        pass

    def test_moddir(self):
        pass

    def test_modname(self):
        pass

    def test_pkgdir(self):
        pass

    def test_pkgname(self):
        self.assertEqual(Utils.pkgname(Utils), "nixt")

    def test_pipxdir(self):
        pass

    def test_skip(self):
        pass

    def test_skipped(self):
        pass

    def test_source(self):
        pass

    def test_spl(self):
        pass

    def test_strptime(self):
        date = time.strptime("2019-3-4 22:22", "%Y-%m-%d %H:%M")
        self.assertTrue(date is not None)

    def test_where(self):
        pass
