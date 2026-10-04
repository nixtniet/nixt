# This file is placed in the Public Domain.


"threads"


import unittest


from typing import List


from nixt.threads import Task, Thread


buffer: List[str] = []


def test():
    "append to buffer."
    buffer.append("test")


class TestTask(unittest.TestCase):

    "thr unittests"

    def test_construct(self):
        "test thr construction." 
        task = Task(test)
        self.assertTrue(type(task), Task)


class TestThread(unittest.TestCase):

    "thread unittests"

    def test_construct(self):
        "test thread construction."
        thr = Thread()
        self.assertTrue(type(thr), Thread)
