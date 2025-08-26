# This file is placed in the Public Domain.


"runtime"


import unittest


from nixt.run import Task


def func():
    return "ok"


class TestRuntime(unittest.TestCase):

    def test_construct(self):
        task = Task(func)
        task.start()
        result = task.join()
        self.assertEqual(result, "ok")
