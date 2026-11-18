# This file is placed in the Public Domain.


"threads"


import unittest


from nixt.tasking import Work


buffer = []


def test():
    "append to buffer."
    buffer.append("test")


class TestTask(unittest.TestCase):

    "thread unittests"

    def test_construct(self):
        "test thread construction."
        work = Work(test)
        self.assertTrue(type(work), Work)
