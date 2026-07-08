# This file is placed in the Public Domain.


"threading"


import unittest


from nixt.defines import Task, Thread


def func():
    return "ok"


class TestTask(unittest.TestCase):

    def test_construct(self):
        task = Task(func)
        self.assertTrue(task)

    def test_join(self):
        task = Task(func)
        task.start()
        result = task.join()
        self.assertEqual(result, "ok")

    def test_run(self):
        pass


class TestThread(unittest.TestCase):

    def test_construct(self):
        thread = Thread()
        self.assertTrue(thread)

    def test_launch(self):
        pass

    def test_clsname(self):
        pass

    def test_name(self):
        pass
