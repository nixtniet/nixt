# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116

"threads"


import unittest


from nixt.threads import Task


def func():
    return "ok"


class TestThread(unittest.TestCase):

    def test_construct(self):
        task = Task(func)
        task.start()
        result = task.join()
        self.assertEqual(result, "ok")
