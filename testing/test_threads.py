# This file is placed in the Public Domain.


"threads"


import unittest


from typing import List


from nixt.threads import Thread, Threading


buffer: List[str] = []


def test():
    "append to buffer."
    buffer.append("test")


class TestThread(unittest.TestCase):

    "thr unittests"

    def test_construct(self):
        "test thr construction." 
        thr = Thread(test)
        self.assertTrue(type(thr), Thread)


class TestThreading(unittest.TestCase):

    "thread unittests"

    def test_construct(self):
        "test thread construction."
        thr = Threading()
        self.assertTrue(type(thr), Threading)
