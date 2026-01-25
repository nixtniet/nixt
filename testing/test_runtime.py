# This file is placed in the Public Domain.


"runtime"


import unittest


import nixt.runtime as TARGET


iface = [
    '__builtins__',
    '__cached__',
    '__doc__',
    '__file__',
    '__loader__',
    '__name__',
    '__package__',
    '__spec__'
]


class TestRuntime(unittest.TestCase):

    def test_interface(self):
        for face in iface:
            self.assertTrue(face in dir(TARGET))
