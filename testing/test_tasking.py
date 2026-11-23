# This file is placed in the Public Domain.


"threads"


import unittest


from nixt.threads import Task


buffer = []


def test():
    "append to buffer."
    buffer.append("test")


class TestTask(unittest.TestCase):

    "thread unittests"

    def test_construct(self):
        "test thread construction."
        task = Task(test)
        self.assertTrue(type(task), Task)
