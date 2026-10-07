# This file is placed in the Public Domain.


"threads"


import unittest


from typing import List


from nixt.tasking import Task, Worker


buffer: List[str] = []


def test():
    "append to buffer."
    buffer.append("test")


class TestWorker(unittest.TestCase):

    "thr unittests"

    def test_construct(self):
        "test thr construction." 
        worker = Worker(test)
        self.assertTrue(type(worker), Worker)


class TestThreading(unittest.TestCase):

    "thread unittests"

    def test_construct(self):
        "test thread construction."
        task = Task()
        self.assertTrue(type(task), Task)
