# This file is placed in the Public Domain.


"runtime"


import unittest


from nixt.thread import Thread 


def func():
    return "ok"


class TestThread(unittest.TestCase):

    def test_construct(self):
        task = Thread(func)
        task.start()
        result = task.join()
        self.assertEqual(result, "ok")
