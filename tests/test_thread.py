# This file is placed in the Public Domain.


import unittest
import time
import threading


from nixt.thread import Thread, Errors, launch, later, line, name


class TestThread(unittest.TestCase):

    def setUp(self):
        Errors.errors = [] 

    def test_thread_init(self):
        pass

    def test_thread_run_success(self):
        pass

    def test_thread_run_exception(self):
        pass

    def test_thread_join(self):
        pass


class TestErrors(unittest.TestCase):

    def setUp(self):
        Errors.errors = []

    def test_errors_storage(self):
        pass


class TestFunctions(unittest.TestCase):

    def setUp(self):
        Errors.errors = []

    def test_launch(self):
        pass

    def test_later(self):
        pass

    def test_line(self):
        pass

    def test_name(self):
        pass

 
if __name__ == '__main__':
    unittest.main()
