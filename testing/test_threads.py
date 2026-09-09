# This file is placed in the Public Domain.


"threading"


import unittest


from nixt.defines import Thr


def func():
    return "ok"


class TestThread(unittest.TestCase):

    def test_task(self):
        thr = Thr(func)
        thr.start()
        result = thr.join()
        self.assertEqual(result, "ok")
